from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from core.security import obtener_usuario_actual
from services.business_logic import obtener_fotos_alumno
from schemas.schemas import FotoResponse

router = APIRouter(prefix="/api/v1/fotos", tags=["Fotos"])

@router.get("/mis-fotos")
def listar_mis_fotos(
    db: Session = Depends(get_db),
    dni_usuario: str = Depends(obtener_usuario_actual)
):
    """
    Retorna el historial de fotos subidas por el alumno autenticado.
    """
    return obtener_fotos_alumno(db=db, dni=dni_usuario)