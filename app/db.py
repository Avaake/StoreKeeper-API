from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask import Flask
from sqlalchemy import MetaData
from app.core import settings


class Base(DeclarativeBase):
    metadata = MetaData(
        naming_convention=settings.db.naming_convention,
    )


class Database:
    def __init__(self, base):
        self.__db = SQLAlchemy(model_class=base)

    def get_db(self) -> SQLAlchemy:
        return self.__db

    def init_app(self, app: Flask):
        self.__db.init_app(app)


db = Database(Base)
