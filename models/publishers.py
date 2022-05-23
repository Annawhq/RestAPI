import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from db_session import SqlAlchemyBase


class Publishers(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'publishers'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    namepublisher = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    address = sqlalchemy.Column(sqlalchemy.String)
    site = sqlalchemy.Column(sqlalchemy.String)

    books = orm.relation("Books", back_populates='publisher')
