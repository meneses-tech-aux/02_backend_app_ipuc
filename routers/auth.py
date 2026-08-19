from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from services.auth_moodle import verificar_credenciales_paideia
from core.security import crear_token_acceso

router = APIRouter(prefix="/api/v1/auth", tags=["Autenticación"])

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

@router.post("/login", response_model=TokenResponse)
def login_for_access_token(credentials: LoginRequest):
    # 1. Verificar contra Moodle (Paideia)
    es_valido = verificar_credenciales_paideia(credentials.username, credentials.password)
    
    if not es_valido:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 2. Si es válido, crear nuestro propio token guardando el DNI en el campo 'sub'
    token_data = {"sub": credentials.username}
    access_token = crear_token_acceso(token_data)
    
    # 3. Enviar al celular
    return {"access_token": access_token, "token_type": "bearer"}