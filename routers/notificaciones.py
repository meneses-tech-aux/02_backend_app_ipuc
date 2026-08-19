from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from core.security import obtener_usuario_actual
from schemas.schemas import NotificacionResponse
from services.business_logic import obtener_notificaciones_activas

router = APIRouter(prefix="/api/v1/notificaciones", tags=["Notificaciones"])

@router.get("/activas", response_model=List[NotificacionResponse])
def listar_notificaciones(
    db: Session = Depends(get_db),
    dni_usuario: str = Depends(obtener_usuario_actual)
):
    """
    Retorna la lista de notificaciones institucionales vigentes.
    Solo accesible para usuarios autenticados.
    """
    return obtener_notificaciones_activas(db=db)