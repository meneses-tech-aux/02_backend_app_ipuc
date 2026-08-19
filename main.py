from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importar todos los routers
from routers import auth, alumnos, fotos, matriculas, beneficios, notificaciones

app = FastAPI(title="API Backend IPUC", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Conectar los endpoints
app.include_router(auth.router)
app.include_router(alumnos.router)
app.include_router(fotos.router)
app.include_router(matriculas.router)
app.include_router(beneficios.router)
app.include_router(notificaciones.router)

@app.get("/")
def health_check():
    return {"status": "ok", "message": "API IPUC corriendo correctamente"}