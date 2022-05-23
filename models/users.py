import datetime
import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from passlib.hash import pbkdf2_sha256 as sha256

import db_session
from db_session import SqlAlchemyBase


class User(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    def __repr__(self):
        return f'<User> {self.id} {self.name} {self.email}'

    def save_to_db(self):
        session = db_session.create_session()
        session.add(self)
        session.commit()

    @classmethod
    def find_by_email(cls, email):
        session = db_session.create_session()
        return session.query(User).filter(User.email == email).first()

    @staticmethod
    def return_all():
        def to_json(x):
            return {
                'email': x.email,
                'password': x.hashed_password
            }
        session = db_session.create_session()
        return {'users': list(map(lambda x: to_json(x), session.query(User).all()))}

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)
