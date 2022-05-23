import datetime
from flask import jsonify, Request
from flask_restful import Resource

import db_session
from models.revoked_tokens import RevokedTokenModel
from models.users import User
from reqparse.login_reqparse import parser
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required,
                                get_jwt_identity, get_jwt)


def revoked_token(jti):
    now = datetime.datetime.now(datetime.timezone.utc)
    token = RevokedTokenModel(jti=jti, created_date=now)
    token.save_to_db()


class UserRegistration(Resource):
    def post(self):
        data = parser.parse_args()
        if User.find_by_email(data['email']):
            return jsonify(
                message='User is already registered')
        else:
            new_user = User(
                name=data['name'],
                email=data['email'],
                hashed_password=User.generate_hash(data['password'])
            )
            try:
                new_user.save_to_db()
                session = db_session.create_session()
                current_request = session.query(User).filter(User.email == data['email']).first()
                access_token = create_access_token(identity=current_request.id)
                refresh_token = create_refresh_token(identity=current_request.id)
                return jsonify(
                    message='User {} was created'.format(data['email']),
                    refreshToken=refresh_token,
                    accessToken=access_token
                )
            except:
                return jsonify(
                    message='Something went wrong')


class UserLogin(Resource):
    def post(self):
        data = parser.parse_args()
        current_user = User.find_by_email(data['email'])
        if not current_user:
            return {'message': 'User {} doesn\'t exist'.format(data['email'])}

        if User.verify_hash(data['password'], current_user.hashed_password):
            time_delta = datetime.timedelta(minutes=15)
            user_dict = current_user.to_dict(only=('id', 'name', 'email'))
            access_token = create_access_token(identity=user_dict,
                                               fresh=time_delta)  # , expires_delta=time_delta
            refresh_token = create_refresh_token(identity=user_dict)
            return jsonify(
                message='Logged in as {}'.format(current_user.email),
                refreshToken=refresh_token,
                accessToken=access_token
            )
        else:
            return jsonify(
                message='Wrong credentials')


class UserLogoutAccess(Resource):
    @jwt_required(fresh=True)
    def post(self):
        jti = get_jwt()['jti']
        try:
            revoked_token(jti)
            return jsonify(
                message='Access token has been revoked')
        except:
            return jsonify(
                message='Wrong credentials')


class UserLogoutRefresh(Resource):
    def post(self):
        return {'message': 'User logout'}


class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        time_delta = datetime.timedelta(minutes=15)
        access_token = create_access_token(identity=current_user, fresh=time_delta)
        return jsonify(access_token=access_token)


class AllUsers(Resource):
    def get(self):
        return User.return_all()

    def delete(self):
        return User.delete_all()


class SecretResource(Resource):
    @jwt_required(fresh=True)
    def get(self):
        return jsonify(
            answer=42
        )