from flask import Flask
from flask_restplus import Api, Resource, fields, inputs

from src.server.instance import server
from src.utils.openTapioca import startNER
from src.environment.instance import env
from src.models.ner import nerResponse
from flask_restplus import reqparse

app, ns = server.app, server.ns
parser = reqparse.RequestParser()
parser.add_argument('title', required=True, help="Title of the data")

class NER(object):
    def __init__(self):
        pass

    def evaluateString(self, userInput): # is_protagonist
        res = startNER(userInput)
        res_map = {}
        res_map['results'] = res
        return res_map

ner = NER()

@ns.route('/ner')
class NEREndpoint(Resource):
    @ns.expect(parser, validate=True)
    @ns.marshal_with(nerResponse)
    @ns.doc(params={
        'title': 'Title of the Data'
        })
    def get(self):
        args = parser.parse_args()
        return ner.evaluateString(args['title'])

