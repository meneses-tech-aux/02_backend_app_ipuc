from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from core.config import settings

# Motor de base de datos
engine = create_engine(settings.DATABASE_URL, echo=True, future=True)

# Fábrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clase base para los modelos ORM
Base = declarative_base()

# Inyección de dependencias para obtener la sesión en los routers
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()