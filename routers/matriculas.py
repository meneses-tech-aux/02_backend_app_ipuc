from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from models.models import Matricula, Alumno
from core.security import obtener_usuario_actual

router = APIRouter(
    prefix="/api/v1/matriculas",
    tags=["Matriculas"]
)

@router.get("/mis-matriculas")
def obtener_mis_matriculas(
    db: Session = Depends(get_db),
    dni_usuario: str = Depends(obtener_usuario_actual) # <-- Bloqueo de seguridad
):
    """
    Retorna todo el historial de matrículas del alumno autenticado.
    """
    # 1. Obtenemos el ID real del alumno a partir de su token
    alumno = db.query(Alumno).filter(Alumno.dni == dni_usuario).first()
    if not alumno:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")

    # 2. Buscamos sus matrículas
    matriculas = db.query(Matricula).filter(
        Matricula.id_alumno == alumno.id
    ).order_by(Matricula.created_at.desc()).all()
    
    if not matriculas:
        raise HTTPException(status_code=404, detail="No se encontraron matrículas para este alumno")
        
    return matriculas