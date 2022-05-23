from flask import jsonify
from flask_restful import abort, Resource
import db_session
from models.authors import Authors
from reqparse.reqparse_authors import parser


def abort_if_author_not_found(author_id):
    session = db_session.create_session()
    author = session.query(Authors).get(author_id)
    if not author:
        abort(404, message=f"Author {author_id} not found")


class AuthorsView(Resource):
    def get(self):
        session = db_session.create_session()
        authors = session.query(Authors).all()
        return [item.to_dict(
            only=('firstname', 'lastname')) for item in authors]

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        new_author = Authors(
            firstname=args['firstname'],
            lastname=args['lastname'])
        session.add(new_author)
        session.commit()
        return jsonify({'success': 'OK'})


class AuthorView(Resource):
    def get(self, author_id):
        abort_if_author_not_found(author_id)
        session = db_session.create_session()
        author = session.query(Authors).get(author_id)
        return jsonify({'Author': author.to_dict(
            only=('firstname', 'lastname'))})

    def delete(self, author_id):
        abort_if_author_not_found(author_id)
        session = db_session.create_session()
        author = session.query(Authors).get(author_id)
        session.delete(author)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, author_id):
        abort_if_author_not_found(author_id)
        args = parser.parse_args()
        session = db_session.create_session()
        author = session.query(Authors).get(author_id)
        if author:
            author.firstname = args['firstname']
            author.lastname = args['lastname']
        else:
            author = Authors(author_id=id, **args)
        session.add(author)
        session.commit()
        return jsonify({'success': 'OK'})