from flask import Flask
from flask_restplus import Api, Resource, fields

from src.server.instance import server
from src.models.property import prop_list, prop_response_list
from src.environment.instance import env
from src.utils.mapper import map_property_batch

app, ns = server.app, server.ns

class PropMapper(object):
    def __init__(self):
        self.property_index = env['PROPERTY_INDEX']

    def search_property_batch(self, properties):
        pl = map_property_batch(properties, self.property_index, server.w2v_model, server.es)
        return {"results": pl}

pm = PropMapper()

@ns.route('/property')
class BulkPropertyMapper(Resource):
    @ns.expect(prop_list, validate=True)
    @ns.marshal_list_with(prop_response_list)
    @ns.doc(params={'item': 'String you want to map to Wikidata Property', 'item_range': 'Range of that Property'})
    def post(self):
        return pm.search_property_batch(ns.payload['properties'])