from pydantic import BaseModel
from typing import Optional
from datetime import date

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