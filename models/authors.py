import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from db_session import SqlAlchemyBase


class Authors(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'authors'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    firstname = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    lastname = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    books = orm.relation('Books', back_populates='author')
