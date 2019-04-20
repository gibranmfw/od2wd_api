from flask import Flask
from flask_restplus import Api, Resource, fields

from server.instance import server
from models.entity import ent, ent_response, ent_list, ent_response_list
from environment.instance import env
from utils.mapper import map_entity, map_entity_batch

app, ns = server.app, server.ns

class EntMapper(object):
    def __init__(self):
        pass

    def search_entity(self, data, context):
        ids, label = map_entity(data, context, server.w2v_model)
        return {"id": ids, "label": label}

    def search_entity_bacth(self, datas):
        el = map_entity_batch(datas, server.w2v_model)
        return {"results": el}

em = EntMapper()

@ns.route('/entity')
class EntityMapper(Resource):
    @ns.expect(ent, validate=True)
    @ns.marshal_with(ent_response)
    @ns.doc(params={'item': 'String you want to map to Wikidata Entity', 'context': 'context of the string you want to map'})
    def post(self):
        return em.search_entity(ns.payload['item'], ns.payload['context'])

@ns.route('/entity/bulk')
class BulkEntityMapper(Resource):
    @ns.expect(ent_list, validate=True)
    @ns.marshal_list_with(ent_response_list)
    @ns.doc(params={'item': 'String you want to map to Wikidata Entity', 'context': 'context of the string you want to map'})
    def post(self):
        return em.search_entity_bacth(ns.payload['entities'])