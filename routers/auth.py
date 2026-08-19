from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from services.auth_moodle import verificar_usuario_paideia
from core.security import crear_token_acceso

router = APIRouter(prefix="/api/v1/auth", tags=["Autenticación"])

class LoginRequest(BaseModel):
    username: str
    password: str | None = None

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_info: dict | None = None

@router.post("/login", response_model=TokenResponse)
def login_for_access_token(credentials: LoginRequest):
    usuario_paideia = verificar_usuario_paideia(credentials.username)
    
    if not usuario_paideia:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El usuario no se encuentra registrado en Paideia Idiomas.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token_data = {
        "sub": str(usuario_paideia["username"]),
        "moodle_id": usuario_paideia.get("id"),
        "fullname": usuario_paideia.get("fullname")
    }
    access_token = crear_token_acceso(token_data)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_info": {
            "id": usuario_paideia.get("id"),
            "username": usuario_paideia.get("username"),
            "fullname": usuario_paideia.get("fullname"),
            "email": usuario_paideia.get("email")
        }
    }