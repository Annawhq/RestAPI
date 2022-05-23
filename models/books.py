import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from db_session import SqlAlchemyBase


class Books(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'books'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    authorid = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('authors.id'))
    publishid = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('publishers.id'))
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    code = sqlalchemy.Column(sqlalchemy.String)
    yearpublish = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    countpage = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    hardcover = sqlalchemy.Column(sqlalchemy.String)
    abstract = sqlalchemy.Column(sqlalchemy.Text)
    status = sqlalchemy.Column(sqlalchemy.Boolean, default=True)

    author = orm.relation('Authors')
    publisher = orm.relation('Publishers')

    def __repr__(self):
        return f'<Book> {self.id}{self.title}{self.status}'
