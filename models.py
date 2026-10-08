import datetime
from peewee import Model, CharField, FloatField, IntegerField, DateTimeField
from database import db

class BaseModel(Model):
    class Meta:
        database = db

class LiquorModel(BaseModel):
    nombre = CharField()
    categoria = CharField()
    precio = FloatField()
    stock = IntegerField(default=0)
    grado_alcohol = FloatField(default=0.0)
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = 'licores'