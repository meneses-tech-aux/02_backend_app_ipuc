from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from models.models import Foto, Alumno
from core.security import obtener_usuario_actual

router = APIRouter(
    prefix="/api/v1/fotos",
    tags=["Fotos"]
)

@router.get("/mis-fotos")
def obtener_mis_fotos(
    db: Session = Depends(get_db),
    dni_usuario: str = Depends(obtener_usuario_actual) # <-- Bloqueo de seguridad
):
    """
    Retorna el historial de fotos subidas por el alumno autenticado.
    """
    alumno = db.query(Alumno).filter(Alumno.dni == dni_usuario).first()
    if not alumno:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")

    fotos = db.query(Foto).filter(
        Foto.id_alumno == alumno.id
    ).order_by(Foto.fecha_subida.desc()).all()
    
    if not fotos:
        raise HTTPException(status_code=404, detail="No se encontraron fotos para este alumno")
        
    return fotos