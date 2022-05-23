from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('firstname', required=True)
parser.add_argument('lastname', required=True)