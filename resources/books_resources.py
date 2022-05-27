from flask import jsonify
from flask_restful import abort, Resource
import db_session
from models.books import Books
from reqparse.reqparse_books import parser


def abort_if_book_not_found(book_id):
    session = db_session.create_session()
    book = session.query(Books).get(book_id)
    if not book:
        abort(404, message=f"Book {book_id} not found")


class BooksView(Resource):
    def get(self):
        session = db_session.create_session()
        books = session.query(Books).all()
        return [item.to_dict(
            only=('author.firstname', 'author.lastname', 'publisher.namepublisher',
                  'publisher.address', 'publisher.site', 'title', 'code', 'yearpublish', 'countpage', 'hardcover',
                  'abstract', 'status')) for item in books]
        #return jsonify({'Books': [item.to_dict(
            #only=('author.firstname', 'author.lastname', 'publisher.namepublisher',
                  #'publisher.address', 'publisher.site', 'title', 'code', 'yearpublish', 'countpage', 'hardcover',
                  #'abstract', 'status')) for item in books]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        flag = True
        if args['status'] == 'False':  # Status transform
            flag = False

        new_book = Books(
            authorid=args['authorid'],
            publishid=args['publishid'],
            title=args['title'],
            code=args['code'],
            yearpublish=args['yearpublish'],
            countpage=args['countpage'],
            hardcover=args['hardcover'],
            abstract=args['abstract'],
            status=flag)
        session.add(new_book)
        session.commit()
        return jsonify({'success': 'OK'})


class BookView(Resource):
    def get(self, book_id):
        abort_if_book_not_found(book_id)
        session = db_session.create_session()
        book = session.query(Books).get(book_id)
        return jsonify({'Book': book.to_dict(
            only=('author.firstname', 'author.lastname', 'publisher.namepublisher',
                  'publisher.address', 'publisher.site', 'title', 'code', 'yearpublish', 'countpage', 'hardcover',
                  'abstract', 'status')
        )})

    def delete(self, book_id):
        abort_if_book_not_found(book_id)
        session = db_session.create_session()
        book = session.query(Books).get(book_id)
        session.delete(book)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, book_id):
        abort_if_book_not_found(book_id)
        args = parser.parse_args()
        session = db_session.create_session()
        book = session.query(Books).get(book_id)
        flag = True
        if args['status'] == 'False':  # Status transform
            flag = False
        if book:
            book.authorid = args['authorid']
            book.publishid = args['publishid']
            book.title = args['title']
            book.code = args['code']
            book.yearpublish = args['yearpublish']
            book.countpage = args['countpage']
            book.hardcover = args['hardcover']
            book.abstract = args['abstract']
            book.status = flag
        else:
            book = Books(book_id=id, **args)
        session.add(book)
        session.commit()
        return jsonify({'success': 'OK'})


class BookSearch(Resource):
    def get(self, search_text):
        session = db_session.create_session()
        result = session.query(Books).filter(Books.title.like('%'+search_text+'%')).all()
        return jsonify([item.to_dict(
            only=('author.firstname', 'author.lastname', 'publisher.namepublisher',
                  'publisher.address', 'publisher.site', 'title', 'code', 'yearpublish', 'countpage', 'hardcover',
                  'abstract', 'status')) for item in result])