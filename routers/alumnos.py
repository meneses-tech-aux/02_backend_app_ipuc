from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from schemas.schemas import CarnetResponse
from services.business_logic import obtener_datos_carnet_estudiante
from core.security import obtener_usuario_actual

router = APIRouter(prefix="/api/v1/alumnos", tags=["Alumnos"])

@router.get("/mi-carnet", response_model=CarnetResponse)
def endpoint_obtener_carnet(
    db: Session = Depends(get_db),
    dni_usuario: str = Depends(obtener_usuario_actual)):
    """
    Retorna los datos del alumno y su matrícula activa para pintar el carnet.
    """
    return obtener_datos_carnet_estudiante(db=db, dni=dni_usuario)