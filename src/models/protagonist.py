from flask_restplus import fields
from src.server.instance import server

protag = server.api.model('linking input', {
    'item': fields.String(required=True, min_length=1, description='String you want to map to Wikidata Entity', example='kelapa gading'),
    'limit': fields.Integer(required=True, description='Limit entity candidates', example=10),
})

protag_response = server.api.model('entity', {
    'id': fields.String(required=True, min_length=1, description='ID of the class', example='Q193545'),
    'label': fields.String(required=True, min_length=1, description='Label of the class', example='Kelapa Gading'),
    'description': fields.String(required=True, min_length=1, description='Description of the class', example='alamat'),
    'score': fields.Float(example='1', description='Confidence score')
})
