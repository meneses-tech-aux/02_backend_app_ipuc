from datetime import date
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.models import Alumno, Matricula, Foto, Beneficio, Notificacion, AppViewer

def obtener_datos_carnet_estudiante(db: Session, dni: str) -> dict:
    alumno = db.query(Alumno).filter(Alumno.dni == str(dni).strip()).first()
    if not alumno:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Alumno con DNI {dni} no encontrado en la base de datos."
        )

    matricula_activa = db.query(Matricula).filter(
        Matricula.id_alumno == alumno.id,
        Matricula.estado == 'ACTIVO'
    ).first()

    if not matricula_activa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="El alumno no tiene matrículas activas registradas."
        )

    foto = db.query(Foto).filter(
        Foto.id_alumno == alumno.id
    ).order_by(Foto.fecha_subida.desc()).first()

    return {
        "nombres": alumno.nombres,
        "apellidos": f"{alumno.apellido_paterno} {alumno.apellido_materno}",
        "tipo_documento": "DOCUMENTO NACIONAL DE IDENTIDAD (DNI)",
        "numero_documento": alumno.dni,
        "codigo_estudiante": alumno.codigo_idiomas,
        "rol": "ESTUDIANTE",
        "clase": matricula_activa.curso,
        "horario": matricula_activa.horario,
        "sede": "PUEBLO LIBRE", 
        "aula": matricula_activa.aula,
        "foto_url": foto.url_s3_foto if foto else None
    }

def obtener_fotos_alumno(db: Session, dni: str) -> List[Foto]:
    alumno = db.query(Alumno).filter(Alumno.dni == str(dni).strip()).first()
    if not alumno:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Alumno con DNI {dni} no encontrado."
        )

    fotos = db.query(Foto).filter(
        Foto.id_alumno == alumno.id
    ).order_by(Foto.fecha_subida.desc()).all()

    if not fotos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontraron fotos para este alumno."
        )
        
    return fotos

def obtener_matriculas_alumno(db: Session, dni: str) -> List[Matricula]:
    alumno = db.query(Alumno).filter(Alumno.dni == str(dni).strip()).first()
    if not alumno:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Alumno con DNI {dni} no encontrado."
        )

    matriculas = db.query(Matricula).filter(
        Matricula.id_alumno == alumno.id
    ).order_by(Matricula.created_at.desc()).all()

    if not matriculas:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontraron matrículas para este alumno."
        )
        
    return matriculas

def obtener_beneficios_activos(db: Session) -> List[Dict[str, Any]]:
    hoy = date.today()
    
    resultados = db.query(Beneficio, AppViewer.fecha_caducidad).join(
        AppViewer, AppViewer.id_beneficios == Beneficio.id
    ).filter(
        AppViewer.estado == 'activo',
        (AppViewer.fecha_caducidad >= hoy) | (AppViewer.fecha_caducidad.is_(None))
    ).order_by(AppViewer.created_at.desc()).all()

    return [
        {
            "id": b.id,
            "titulo": b.titulo,
            "descripcion": b.descripcion,
            "fecha_caducidad": fc
        }
        for b, fc in resultados
    ]

def obtener_notificaciones_activas(db: Session) -> List[Dict[str, Any]]:
    hoy = date.today()
    
    resultados = db.query(Notificacion, AppViewer.fecha_caducidad).join(
        AppViewer, AppViewer.id_notificaciones == Notificacion.id
    ).filter(
        AppViewer.estado == 'activo',
        (AppViewer.fecha_caducidad >= hoy) | (AppViewer.fecha_caducidad.is_(None))
    ).order_by(AppViewer.created_at.desc()).all()

    return [
        {
            "id": n.id,
            "descripcion": n.descripcion,
            "fecha_caducidad": fc
        }
        for n, fc in resultados
    ]