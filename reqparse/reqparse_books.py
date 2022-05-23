from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('authorid', required=True)
parser.add_argument('publishid', required=True)
parser.add_argument('title', required=True)
parser.add_argument('code', required=True)
parser.add_argument('yearpublish', required=True)
parser.add_argument('countpage', required=True)
parser.add_argument('hardcover', required=True)
parser.add_argument('abstract', required=True)
parser.add_argument('status', required=True)

