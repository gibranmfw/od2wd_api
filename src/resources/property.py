from flask import Flask
from flask_restplus import Api, Resource, fields

from src.server.instance import server
from src.models.property import prop_list, prop_response_list, props
from src.environment.instance import env
from src.utils.mapper import map_property_batch, map_property
from flask_restplus import reqparse

app, ns = server.app, server.ns
range_map = {
    'string':'String',
    'wikibaseitem':'WikibaseItem',
    'quantity':'Quantity',
    'globecoordinate':'GlobeCoordinate',
    'time':'Time',
    'url':'Url'
    }

class PropMapper(object):
    def __init__(self):
        self.property_index = env['PROPERTY_INDEX']

    def search_property(self, item, item_range, limit):
        res_map = {}
        cand_list = []
        ir = item_range.lower()
        ir = range_map[ir]
        cand_props = map_property(item, ir, self.property_index, server.w2v_model, server.es, limit)
        for key, value in cand_props.items():
            res = {"id": value['id'], "label": value['label'], "description": value['description'], "score": key}
            cand_list.append(res)
        res_map['item'] = item
        res_map['map_to'] = cand_list
        return res_map

    def search_property_batch(self, properties):
        pl = map_property_batch(properties, self.property_index, server.w2v_model, server.es)
        return {"results": pl}

pm = PropMapper()

parser = reqparse.RequestParser()
parser.add_argument('item', required=True, help="String you want to map to Wikidata Entity")
parser.add_argument('item_range', required=True)
parser.add_argument('limit', required=True, type=int)

@ns.route('/property')
class PropertyMapper(Resource):
    @ns.expect(parser, validate=True)
    @ns.marshal_with(props)
    @ns.doc(params={
        'item': 'String you want to map to Wikidata Property', 
        'item_range': 'Range of that Property',
        'limit': 'Limit entity candidates'
        })
    def get(self):
        args = parser.parse_args()
        return pm.search_property(args['item'], args['item_range'], args['limit'])

    @ns.expect(prop_list, validate=True)
    @ns.marshal_list_with(prop_response_list)
    @ns.doc(params={
        'item': 'String you want to map to Wikidata Property', 
        'item_range': 'Range of that Property',
        'limit': 'Limit entity candidates'
        })
    def post(self):
        return pm.search_property_batch(ns.payload['properties'])
