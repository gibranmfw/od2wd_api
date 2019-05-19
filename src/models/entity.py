from flask_restplus import fields
from src.server.instance import server

ent = server.api.model('linking input', {
    'item': fields.String(required=True, min_length=1, description='String you want to map to Wikidata Entity', example='kelapa gading'),
    'context': fields.String(required=True, min_length=1, description='Context of the string you want to map', example='kecamatan'),
    'limit': fields.Integer(required=True, description='Limit entity candidates', example=10),
    'is_protagonist': fields.Boolean(required=True, description='True if the entitiy is protagonist, false if not', example=False, default=False)
})

ent_response = server.api.model('entity', {
    'id': fields.String(required=True, min_length=1, description='ID of the Entity', example='Q193545'),
    'label': fields.String(required=True, min_length=1, description='Label of the Entity', example='Kelapa Gading'),
    'description': fields.String(required=True, min_length=1, description='Description of the entity', example='alamat'),
    'score': fields.Float(example='1', description='Confidence score')
})

ents = server.api.model('candidate entities', {
    'item': fields.String(required=True, min_length=1, description='String you want to map to Wikidata Entity', example='kelapa gading'),
    'link_to': fields.List(fields.Nested(ent_response))
})

ent_list = server.api.model('bulk linking', {
    "entities": fields.List(fields.Nested(ent))
})

ent_response_list = server.api.model('linking response', {
    "results": fields.List(fields.Nested(ents))
})