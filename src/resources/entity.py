from flask import Flask
from flask_restplus import Api, Resource, fields

from src.server.instance import server
from src.models.entity import ent_list, ent_response_list
from src.environment.instance import env
from src.utils.mapper import map_entity_batch

app, ns = server.app, server.ns

class EntMapper(object):
    def __init__(self):
        pass

    def search_entity_bacth(self, datas):
        el = map_entity_batch(datas, server.w2v_model)
        return {"results": el}

em = EntMapper()

@ns.route('/entity')
class BulkEntityMapper(Resource):
    @ns.expect(ent_list, validate=True)
    @ns.marshal_list_with(ent_response_list)
    @ns.doc(params={
        'item': 'String you want to map to Wikidata Entity', 
        'context': 'context of the string you want to map',
        'limit': 'Limit entity candidates',
        'is_protagonist': 'True if the entitiy is protagonist, false if not'
        })
    def post(self):
        return em.search_entity_bacth(ns.payload['entities'])
