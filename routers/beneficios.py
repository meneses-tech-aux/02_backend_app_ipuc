from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from core.security import obtener_usuario_actual
from schemas.schemas import BeneficioResponse
from services.business_logic import obtener_beneficios_activos

router = APIRouter(prefix="/api/v1/beneficios", tags=["Beneficios (Cupones)"])

@router.get("/activos", response_model=List[BeneficioResponse])
def listar_beneficios(
    db: Session = Depends(get_db),
    dni_usuario: str = Depends(obtener_usuario_actual)
):
    """
    Retorna la lista de cupones/beneficios activos.
    Solo accesible para usuarios autenticados.
    """
    return obtener_beneficios_activos(db=db)