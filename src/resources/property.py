from flask import Flask
from flask_restplus import Api, Resource, fields

from server.instance import server
from models.property import prop, prop_response, prop_list, prop_response_list
from environment.instance import env
from utils.mapper import map_property, map_property_batch

app, ns = server.app, server.ns

class PropMapper(object):
    def __init__(self):
        self.property_index = env['PROPERTY_INDEX']

    def search_property(self, item, item_type):
        ids, label = map_property(item, item_type, self.property_index, server.w2v_model, server.es)
        return {"id": ids, "label": label}

    def search_property_batch(self, properties):
        pl = map_property_batch(properties, self.property_index, server.w2v_model, server.es)
        return {"results": pl}

pm = PropMapper()

@ns.route('/property')
class PropertyMapper(Resource):
    @ns.expect(prop, validate=True)
    @ns.marshal_with(prop_response)
    @ns.doc(params={'item': 'String you want to map to Wikidata Property', 'item_range': 'Range of that Property'})
    def post(self):
        return pm.search_property(ns.payload['item'], ns.payload['item_range'])

@ns.route('/property/bulk')
class BulkPropertyMapper(Resource):
    @ns.expect(prop_list, validate=True)
    @ns.marshal_list_with(prop_response_list)
    @ns.doc(params={'item': 'String you want to map to Wikidata Property', 'item_range': 'Range of that Property'})
    def post(self):
        return pm.search_property_batch(ns.payload['properties'])