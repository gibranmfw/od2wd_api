from flask_restplus import fields
from src.server.instance import server

prop = server.api.model('prop', {
    'item': fields.String(required=True, min_length=1, description='String you want to map to Wikidata Property', example='alamat'),
    'item_range': fields.String(required=True, min_length=1, description='Range of that Property', example='String')
})

prop_response = server.api.model('prop_response', {
    'id': fields.String(required=True, min_length=1, description='ID of the Property', example='P6375'),
    'label': fields.String(required=True, min_length=1, description='Label of the Property', example='alamat')
})

prop_list = server.api.model('prop_list', {
    'properties': fields.List(fields.Nested(prop))
})

prop_response_list = server.api.model('prop_response_list', {
    'results': fields.List(fields.Nested(prop_response))
})