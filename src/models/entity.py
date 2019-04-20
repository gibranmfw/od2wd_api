from flask_restplus import fields
from src.server.instance import server

ent = server.api.model('ent', {
    'item': fields.String(required=True, min_length=1, description='String you want to map to Wikidata Entity', example='kelapa gading'),
    'context': fields.String(required=True, min_length=1, description='context of the string you want to map', example='kecamatan')
})

ent_response = server.api.model('ent_response', {
    'id': fields.String(required=True, min_length=1, description='ID of the Entity', example='Q193545'),
    'label': fields.String(required=True, min_length=1, description='Label of the Entity', example='Kelapa Gading')
})

ent_list = server.api.model('ent_list', {
    "entities": fields.List(fields.Nested(ent))
})

ent_response_list = server.api.model('ent_response_list', {
    "results": fields.List(fields.Nested(ent_response))
})