from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from core.config import settings

# Usamos HTTPBearer para que Swagger solo pida el campo de token
security = HTTPBearer()

def crear_token_acceso(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    # Firma el token con tu clave secreta
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def obtener_usuario_actual(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """
    Dependencia para proteger las rutas.
    Extrae el token del header 'Authorization: Bearer <token>', valida la firma y extrae el DNI.
    """
    token = credentials.credentials  # Obtiene el string limpio del token

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
        return dni  # Retorna el DNI del usuario autenticado
    except JWTError:
        raise credentials_exception