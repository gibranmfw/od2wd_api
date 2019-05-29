from flask import Flask
from flask_restplus import Api, Resource, fields, inputs

from src.server.instance import server
from src.models.entity import ent_list, ent_response_list, ent, ents
from src.environment.instance import env
from src.utils.mapper import map_entity_batch, map_entity
from flask_restplus import reqparse

app, ns = server.app, server.ns

parser = reqparse.RequestParser()
parser.add_argument('item', required=True, help="String you want to map to Wikidata Entity")
parser.add_argument('context', required=True)
parser.add_argument('limit', required=True, type=int)
parser.add_argument('is_protagonist', required=True, type=inputs.boolean)

class EntMapper(object):
    def __init__(self):
        pass

    def search_entity(self, item, context, limit, is_protagonist):
        el = map_entity(item, context, server.w2v_model, limit, is_protagonist)
        res_map = {}
        cand_list = []
        for key, value in el.items():
            for item in value:
                res = {"id": item['id'], "label": item['label'], "description": item['description'], 'score': key}
                cand_list.append(res)
                if(len(cand_list) > limit):
                    break

            if(len(cand_list) > limit):
                break

        res_map['item'] = item
        res_map['link_to'] = cand_list
        return res_map

    def search_entity_bacth(self, datas):
        el = map_entity_batch(datas, server.w2v_model)
        return {"results": el}

em = EntMapper()

@ns.route('/entity')
class EntityMapper(Resource):
    @ns.expect(parser, validate=True)
    @ns.marshal_with(ents)
    @ns.doc(params={
        'item': 'String you want to map to Wikidata Entity',
        'context': 'context of the string you want to map',
        'limit': 'Limit entity candidates',
        'is_protagonist': 'True if the entitiy is protagonist, false if not'
        })
    def get(self):
        args = parser.parse_args()
        return em.search_entity(args['item'], args['context'], args['limit'], args['is_protagonist'])

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


