from flask_restplus import fields
from src.server.instance import server

protag = server.api.model('protagonist input', {
    'item': fields.String(required=True, min_length=1, description='String you want to map to Wikidata Entity', example='nama sekolah'),
    'limit': fields.Integer(required=True, description='Limit entity candidates', example=10),
})

protag_response = server.api.model('protagonist', {
    'id': fields.String(required=True, min_length=1, description='ID of the class', example='Q3914'),
    'label': fields.String(required=True, min_length=1, description='Label of the class', example='sekolah'),
    'description': fields.String(required=True, min_length=1, description='Description of the class', example='institution designed to teach students under the direction of teachers'),
    'score': fields.Float(example=1, description='Confidence score')
})

protag_response_list = server.api.model('protagonist_candidates_list', {
    'results': fields.List(fields.Nested(protag_response))
})
