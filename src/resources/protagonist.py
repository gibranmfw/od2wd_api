from flask import Flask
from flask_restplus import Api, Resource, fields

from src.server.instance import server
from src.models.protagonist import protag, protag_response_list
from src.environment.instance import env
from src.utils.mapper import protagonist_mapping
from flask_restplus import reqparse

app, ns = server.app, server.ns

class ProtagMapper(object):
    def __init__(self):
        pass

    def map_protagonist(self, protagonist, limit):
        pl = protagonist_mapping(protagonist, limit, server.w2v_model)
        return {"results": pl}

pm = ProtagMapper()

parser = reqparse.RequestParser()
parser.add_argument('item', required=True, help="String you want to map to Wikidata Entity")
parser.add_argument('limit', required=True, type=int)

@ns.route('/protagonist')
class ProtagonistMapper(Resource):
    @ns.expect(parser, validate=True)
    @ns.marshal_list_with(protag_response_list)
    @ns.doc(params={
        'item': 'String you want to map to Wikidata Entity', 
        'limit': 'Limit entity candidates'
        })
    def get(self):
        args = parser.parse_args()
        return pm.map_protagonist(args['item'], args['limit'])
        
