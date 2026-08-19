from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime


# --- Esquemas de Respuesta para el Carnet ---
class CarnetResponse(BaseModel):
    nombres: str
    apellidos: str
    tipo_documento: str
    numero_documento: str
    codigo_estudiante: str
    rol: str
    clase: str
    horario: str
    sede: str
    aula: str
    foto_url: Optional[str] = None

    class Config:
        from_attributes = True


class BeneficioResponse(BaseModel):
    id: int
    titulo: str
    descripcion: str
    fecha_caducidad: Optional[date] = None

    class Config:
        from_attributes = True

class NotificacionResponse(BaseModel):
    id: int
    descripcion: str
    fecha_caducidad: Optional[date] = None

    class Config:
        from_attributes = True
        
class FotoResponse(BaseModel):
    id: int
    url_s3_foto: str
    fecha_subida: datetime  # o date, según el tipo que uses

    class Config:
        from_attributes = True