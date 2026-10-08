from fastapi import FastAPI, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from database import db
from models import LiquorModel, UserModel
from schemas import LiquorCreateSchema, LiquorUpdateSchema
from services import LiquorService

app = FastAPI(title="Licorería Central - Sistema de Gestión")

@app.on_event("startup")
def startup():
    if db.is_closed():
        db.connect()
    db.create_tables([LiquorModel, UserModel])

    # Semilla inicial de licores
    if LiquorModel.select().count() == 0:
        LiquorService.register_liquor(LiquorCreateSchema(
            nombre="Pisco Quebranta 750ml", categoria="Pisco", precio=48.0, stock=12, grado_alcohol=42.0
        ))
        LiquorService.register_liquor(LiquorCreateSchema(
            nombre="Whisky Black Label 1L", categoria="Whisky", precio=139.0, stock=3, grado_alcohol=40.0
        ))

@app.on_event("shutdown")
def shutdown():
    if not db.is_closed():
        db.close()

# --- ENDPOINTS CRUD REST (Semana 4) ---
@app.get("/api/licores")
def get_all():
    return {"success": True, "data": LiquorService.list_inventory()}

# En main.py
@app.get("/api/licores/{licor_id}")
def get_by_id(licor_id: int):
    item = LiquorService.get_liquor_by_id(licor_id)
    if not item:
        raise HTTPException(status_code=404, detail="Licor no encontrado")
    return {"success": True, "data": item}

@app.post("/api/licores", status_code=status.HTTP_201_CREATED)
def create(schema: LiquorCreateSchema):
    item = LiquorService.register_liquor(schema)
    return {"success": True, "message": "Licor registrado", "id": item.id}

@app.put("/api/licores/{licor_id}")
def update(licor_id: int, schema: LiquorUpdateSchema):
    updated = LiquorService.update_liquor(licor_id, schema)
    if not updated:
        raise HTTPException(status_code=404, detail="Licor no encontrado")
    return {"success": True, "message": "Licor actualizado"}

@app.delete("/api/licores/{licor_id}")
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