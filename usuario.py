from flask_login import UserMixin
from peewee import Model, AutoField, CharField
from modelos import db
import bcrypt

class Usuario(UserMixin, Model):
    id = AutoField()
    nome = CharField()
    email = CharField(unique=True)
    senha = CharField()

    class Meta():
        database = db

    @classmethod
    def get_by_id(cls, user_id):
        return cls.get(cls.id == user_id)
    
    @classmethod
    def get_by_email(cls, email):
        return cls.get(cls.email == email)
    
    def set_password(self, password):
        self.senha = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        self.save()

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.senha.encode('utf-8'))