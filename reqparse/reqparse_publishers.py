from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('namepublisher', required=True)
parser.add_argument('address', required=True)
parser.add_argument('site', required=True)
