from peewee import Model, CharField, FloatField, IntegerField, DateTimeField
import datetime
from database import db
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class BaseModel(Model):
    class Meta:
        database = db

# Entidad Licor
class LiquorModel(BaseModel):
    nombre = CharField()
    categoria = CharField()
    precio = FloatField()
    stock = IntegerField(default=0)
    grado_alcohol = FloatField(default=0.0)
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = 'licores'

# Entidad Usuario con Hashing de Contraseñas (OWASP)
class UserModel(BaseModel):
    email = CharField(unique=True)
    password_hash = CharField()

    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.password_hash)

    class Meta:
        table_name = 'usuarios'