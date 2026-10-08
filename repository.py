from models import LiquorModel
from typing import List, Optional

class LiquorRepository:

    @staticmethod
    def get_all() -> List[LiquorModel]:
        return list(LiquorModel.select().order_by(LiquorModel.id.desc()))

    @staticmethod
    def get_by_id(liquor_id: int) -> Optional[LiquorModel]:
        return LiquorModel.get_or_none(LiquorModel.id == liquor_id)

    @staticmethod
    def create(data: dict) -> LiquorModel:
        return LiquorModel.create(**data)

    @staticmethod
    def update(liquor_id: int, data: dict) -> Optional[LiquorModel]:
        liquor = LiquorModel.get_or_none(LiquorModel.id == liquor_id)
        if liquor:
            for key, value in data.items():
                if value is not None:
                    setattr(liquor, key, value)
            liquor.save()
        return liquor

    @staticmethod
    def delete(liquor_id: int) -> bool:
        liquor = LiquorModel.get_or_none(LiquorModel.id == liquor_id)
        if liquor:
            liquor.delete_instance()
            return True
        return False