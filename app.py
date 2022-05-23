from datetime import timedelta
from flask import Flask, request
from flask_jwt_extended import JWTManager
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from models.authors import *
from models.publishers import *
from models.books import *
from models.revoked_tokens import *
import db_session
from resources import books_resources, authors_resources, publishers_resources, login_resources
from flask_ngrok import run_with_ngrok


app = Flask(__name__)
run_with_ngrok(app)
app.config['SECRET_KEY'] = 'anna_secret_key'
app.config['JWT_SECRET_KEY'] = 'jwt-secret-anna'
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=1)
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
api = Api(app, catch_all_404s=True)
jwt = JWTManager(app)


db_session.global_init()
api.add_resource(books_resources.BooksView, '/books')
api.add_resource(books_resources.BookView, '/book/<int:book_id>')
api.add_resource(authors_resources.AuthorsView, '/authors')
api.add_resource(authors_resources.AuthorView, '/author/<int:author_id>')
api.add_resource(publishers_resources.PublishersView, '/publishers')
api.add_resource(publishers_resources.PublisherView, '/publisher/<int:publisher_id>')
api.add_resource(books_resources.BookSearch, '/books/<search_text>')

api.add_resource(login_resources.UserRegistration, '/registration')
api.add_resource(login_resources.UserLogin, '/login')
api.add_resource(login_resources.UserLogoutAccess, '/logout/access')
api.add_resource(login_resources.UserLogoutRefresh, '/logout/refresh')
api.add_resource(login_resources.TokenRefresh, '/token/refresh')
api.add_resource(login_resources.AllUsers, '/users')
api.add_resource(login_resources.SecretResource, '/secret')


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    token = RevokedTokenModel.is_jti_blacklisted(jti)
    return token is not None


@app.route("/")
def hello():
    return "Hello"


if __name__ == '__main__':
    app.run()