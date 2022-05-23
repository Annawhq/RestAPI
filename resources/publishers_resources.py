from flask import jsonify
from flask_restful import abort, Resource
import db_session
from models.publishers import Publishers
from reqparse.reqparse_publishers import parser


def abort_if_publisher_not_found(publisher_id):
    session = db_session.create_session()
    publisher = session.query(Publishers).get(publisher_id)
    if not publisher:
        abort(404, message=f"Publisher {publisher_id} not found")


class PublishersView(Resource):
    def get(self):
        session = db_session.create_session()
        publishers = session.query(Publishers).all()
        return [item.to_dict(
            only=('namepublisher', 'address', 'site')) for item in publishers]

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        new_publisher = Publishers(
            site=args['site'],
            address=args['address'],
            namepublisher=args['namepublisher'])
        session.add(new_publisher)
        session.commit()
        return jsonify({'success': 'OK'})


class PublisherView(Resource):
    def get(self, publisher_id):
        abort_if_publisher_not_found(publisher_id)
        session = db_session.create_session()
        publisher = session.query(Publishers).get(publisher_id)
        return jsonify({'Publisher': publisher.to_dict(
            only=('namepublisher', 'address', 'site'))})

    def delete(self, publisher_id):
        abort_if_publisher_not_found(publisher_id)
        session = db_session.create_session()
        publisher = session.query(Publishers).get(publisher_id)
        session.delete(publisher)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, publisher_id):
        abort_if_publisher_not_found(publisher_id)
        args = parser.parse_args()
        session = db_session.create_session()
        publisher = session.query(Publishers).get(publisher_id)
        if publisher:
            publisher.namepublisher = args['namepublisher']
            publisher.address = args['address']
            publisher.site = args['site']
        else:
            publisher = Publishers(publisher_id=id, **args)
        session.add(publisher)
        session.commit()
        return jsonify({'success': 'OK'})