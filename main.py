from contextlib import asynccontextmanager
from fastapi import FastAPI, Header, Depends, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from database import db
from models import LiquorModel
from schemas import LiquorCreateSchema, LiquorUpdateSchema
from services import LiquorService

app = FastAPI(title="Licorería Central - Sistema de Gestión")

@asynccontextmanager
async def lifespan(app: FastAPI):
    if db.is_closed():
        db.connect()
    db.create_tables([LiquorModel])

    # Semilla inicial
    if LiquorModel.select().count() == 0:
        LiquorService.register_liquor(LiquorCreateSchema(
            nombre="Pisco Quebranta 750ml", categoria="Pisco", precio=48.0, stock=12, grado_alcohol=42.0
        ))
        LiquorService.register_liquor(LiquorCreateSchema(
            nombre="Whisky Black Label 1L", categoria="Whisky", precio=139.0, stock=3, grado_alcohol=40.0
        ))
    yield
    if not db.is_closed():
        db.close()

app = FastAPI(title="Licorería Central - Sistema de Gestión", lifespan=lifespan)

# Clave secreta requerida
ADMIN_SECRET_KEY = "licoreria-admin-2026"

def verificar_admin(x_api_key: str = Header(..., alias="X-API-Key")):
    if x_api_key != ADMIN_SECRET_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Acceso denegado: Clave de administración no válida o ausente."
        )

# CRUD Endpoints

@app.get("/api/licores")
def get_all():
    return {"success": True, "data": LiquorService.list_inventory()}

@app.get("/api/licores/{licor_id}")
def get_by_id(licor_id: int):
    item = LiquorService.get_liquor_by_id(licor_id)
    if not item:
        raise HTTPException(status_code=404, detail="Licor no encontrado")
    return {"success": True, "data": item}

@app.post("/api/licores", status_code=status.HTTP_201_CREATED, dependencies=[Depends(verificar_admin)])
def create(schema: LiquorCreateSchema):
    item = LiquorService.register_liquor(schema)
    return {"success": True, "message": "Licor registrado", "id": item.id}

@app.put("/api/licores/{licor_id}", dependencies=[Depends(verificar_admin)])
def update(licor_id: int, schema: LiquorUpdateSchema):
    updated = LiquorService.update_liquor(licor_id, schema)
    if not updated:
        raise HTTPException(status_code=404, detail="Licor no encontrado")
    return {"success": True, "message": "Licor actualizado"}

@app.delete("/api/licores/{licor_id}", dependencies=[Depends(verificar_admin)])
def delete(licor_id: int):
    success = LiquorService.remove_liquor(licor_id)
    if not success:
        raise HTTPException(status_code=404, detail="Licor no encontrado")
    return {"success": True, "message": "Licor eliminado"}

# Montar interfaz Frontend
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def serve_index():
    return FileResponse("static/index.html")

@app.get("/editar")
def serve_editar():
    return FileResponse("static/editar.html")