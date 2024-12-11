from peewee import MySQLDatabase, Model, CharField, TextField, ForeignKeyField
import os
from dotenv import load_dotenv

load_dotenv()

db = MySQLDatabase(
    os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT"))
)

from usuario import Usuario

class Info(Model):
    nome = CharField()
    bio = TextField()
    foto = CharField(null = True)
    usuario = ForeignKeyField(Usuario, backref='info')

    class Meta:
        database = db


class Curriculo(Model):
    experiencia = TextField()
    educacao = TextField()
    usuario = ForeignKeyField(Usuario, backref='curriculos')

    class Meta:
        database = db

class Projeto(Model):
    titulo = CharField()
    descricao = TextField()
    usuario = ForeignKeyField(Usuario, backref='projetos')

    class Meta:
        database = db


class Contato(Model):
    email = CharField()
    telefone = CharField()
    usuario = ForeignKeyField(Usuario, backref='contatos')

    class Meta:
        database = db

def create_tables():
    with db.connection_context():
        db.create_tables([Info, Curriculo, Projeto, Contato, Usuario])