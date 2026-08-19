from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from core.config import settings

# FastAPI usará esto para buscar el token en la cabecera (Header) de las peticiones HTTP
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def crear_token_acceso(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    # Firma el token con tu clave secreta
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def obtener_usuario_actual(token: str = Depends(oauth2_scheme)):
    """
    Esta función se usará como dependencia en las rutas para protegerlas.
    Lee el token del celular, verifica que no haya expirado y extrae el DNI del usuario.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        dni: str = payload.get("sub")
        if dni is None:
            raise credentials_exception
        return dni # Retornamos el DNI del usuario logueado
    except JWTError:
        raise credentials_exception