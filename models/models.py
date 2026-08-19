from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, ForeignKey, Text, func
from sqlalchemy.orm import relationship
from core.database import Base

# 1. Tabla Alumno
class Alumno(Base):
    __tablename__ = "alumno"

    id = Column(Integer, primary_key=True, index=True)
    id_origen = Column(Integer, unique=True, nullable=True)
    codigo_idiomas = Column(String(50), unique=True, nullable=False)
    apellido_paterno = Column(String(100), nullable=False)
    apellido_materno = Column(String(100), nullable=False)
    nombres = Column(String(100), nullable=False)
    correo = Column(String(150), nullable=False, index=True)
    dni = Column(String(15), nullable=False, index=True)
    fecha_nacimiento = Column(Date, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    # Relaciones
    fotos = relationship("Foto", back_populates="alumno", cascade="all, delete-orphan")
    matriculas = relationship("Matricula", back_populates="alumno", cascade="all, delete-orphan")


# 2. Tabla Fotos
class Foto(Base):
    __tablename__ = "fotos"

    id = Column(Integer, primary_key=True, index=True)
    url_s3_foto = Column(Text, nullable=False)
    consentimiento = Column(Boolean, default=False)
    menor_de_edad = Column(Boolean, default=False)
    estado = Column(String(20), default="pendiente")
    fecha_subida = Column(DateTime, server_default=func.now())
    id_alumno = Column(Integer, ForeignKey("alumno.id", ondelete="CASCADE"), nullable=False)

    # Relación
    alumno = relationship("Alumno", back_populates="fotos")


# 3. Tabla Matricula
class Matricula(Base):
    __tablename__ = "matricula"

    id = Column(Integer, primary_key=True, index=True)
    id_origen = Column(Integer, unique=True, nullable=True)
    tipo_periodo = Column(String(50), nullable=False)
    mes_matricula = Column(String(20), nullable=False)
    aula = Column(String(50), nullable=False)
    curso = Column(String(150), nullable=False)
    horario = Column(String(100), nullable=False)
    estado = Column(String(20), nullable=False, index=True)
    id_alumno = Column(Integer, ForeignKey("alumno.id", ondelete="CASCADE"), nullable=False, index=True)
    created_at = Column(DateTime, server_default=func.now())

    # Relación
    alumno = relationship("Alumno", back_populates="matriculas")


# 4. Tabla Notificaciones
class Notificacion(Base):
    __tablename__ = "notificaciones"

    id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    # Relación
    viewers = relationship("AppViewer", back_populates="notificacion", cascade="all, delete-orphan")


# 5. Tabla Beneficios
class Beneficio(Base):
    __tablename__ = "beneficios"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(150), nullable=False)
    descripcion = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    # Relación
    viewers = relationship("AppViewer", back_populates="beneficio", cascade="all, delete-orphan")


# 6. Tabla App_Viewer
class AppViewer(Base):
    __tablename__ = "app_viewer"

    id = Column(Integer, primary_key=True, index=True)
    id_notificaciones = Column(Integer, ForeignKey("notificaciones.id", ondelete="CASCADE"), nullable=True)
    id_beneficios = Column(Integer, ForeignKey("beneficios.id", ondelete="CASCADE"), nullable=True)
    estado = Column(String(20), default="activo")
    fecha_caducidad = Column(Date, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    # Relaciones
    notificacion = relationship("Notificacion", back_populates="viewers")
    beneficio = relationship("Beneficio", back_populates="viewers")