import html
from repository import LiquorRepository
from schemas import LiquorCreateSchema, LiquorUpdateSchema

class LiquorService:
    """Responsabilidad Única: Reglas de negocio y sanitización de datos"""

    @staticmethod
    def sanitize(text: str) -> str:
        # Sanitización contra vulnerabilidades Cross-Site Scripting (XSS)
        return html.escape(text.strip())

    @classmethod
    def list_inventory(cls):
        items = LiquorRepository.get_all()
        return [
            {
                "id": item.id,
                "nombre": item.nombre,
                "categoria": item.categoria,
                "precio": item.precio,
                "stock": item.stock,
                "grado_alcohol": item.grado_alcohol,
                "stock_critico": item.stock < 5 # Regla de negocio
            }
            for item in items
        ]

    @classmethod
    def register_liquor(cls, schema: LiquorCreateSchema):
        data = schema.model_dump()
        data["nombre"] = cls.sanitize(data["nombre"])
        data["categoria"] = cls.sanitize(data["categoria"])
        return LiquorRepository.create(data)

    @classmethod
    def update_liquor(cls, liquor_id: int, schema: LiquorUpdateSchema):
        data = schema.model_dump(exclude_unset=True)
        if "nombre" in data and data["nombre"]:
            data["nombre"] = cls.sanitize(data["nombre"])
        if "categoria" in data and data["categoria"]:
            data["categoria"] = cls.sanitize(data["categoria"])
        return LiquorRepository.update(liquor_id, data)

    @classmethod
    def remove_liquor(cls, liquor_id: int) -> bool:
        return LiquorRepository.delete(liquor_id)

    @classmethod
    def get_liquor_by_id(cls, liquor_id: int):
        item = LiquorRepository.get_by_id(liquor_id)
        if not item:
            return None
        return {
            "id": item.id,
            "nombre": item.nombre,
            "categoria": item.categoria,
            "precio": item.precio,
            "stock": item.stock,
            "grado_alcohol": item.grado_alcohol
        }