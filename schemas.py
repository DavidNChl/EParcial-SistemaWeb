from pydantic import BaseModel, Field
from typing import Optional

class LiquorCreateSchema(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    categoria: str = Field(..., min_length=2)
    precio: float = Field(..., gt=0)
    stock: int = Field(0, ge=0)
    grado_alcohol: Optional[float] = Field(0.0, ge=0)

class LiquorUpdateSchema(BaseModel):
    nombre: Optional[str] = None
    categoria: Optional[str] = None
    precio: Optional[float] = None
    stock: Optional[int] = None
    grado_alcohol: Optional[float] = None