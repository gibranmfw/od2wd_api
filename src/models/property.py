from flask_restplus import fields
from src.server.instance import server

prop = server.api.model('mapping input', {
    'item': fields.String(required=True, min_length=1, description='String you want to map to Wikidata Property', example='alamat'),
    'item_range': fields.String(required=True, min_length=1, description='Range of that Property', example='String'),
    'limit': fields.Integer(required=True, description='Limit entity candidates', example=10)
})

prop_response = server.api.model('property', {
    'id': fields.String(required=True, min_length=1, description='ID of the Property', example='P6375'),
    'label': fields.String(required=True, min_length=1, description='Label of the Property', example='alamat'),
    'score': fields.Float(example='1', description='Confidence score')
})

props = server.api.model('candidate properties', {
    'item': fields.String(required=True, min_length=1, description='String you want to map to Wikidata Property', example='alamat'),
    'map_to': fields.List(fields.Nested(prop_response))
})

prop_list = server.api.model('bulk mapping', {
    'properties': fields.List(fields.Nested(prop))
})

prop_response_list = server.api.model('mapping responses', {
    'results': fields.List(fields.Nested(props))
})