from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from core.security import obtener_usuario_actual
from services.business_logic import obtener_matriculas_alumno
from schemas.schemas import MatriculaResponse  # Asegúrate de importar el esquema correspondiente si lo usas

router = APIRouter(prefix="/api/v1/matriculas", tags=["Matriculas"])

@router.get("/mis-matriculas")
def listar_mis_matriculas(
    db: Session = Depends(get_db),
    dni_usuario: str = Depends(obtener_usuario_actual)
):
    """
    Retorna todo el historial de matrículas del alumno autenticado.
    """
    return obtener_matriculas_alumno(db=db, dni=dni_usuario)