from flask import Flask
from flask_restplus import Api, Resource, fields

from src.server.instance import server
from src.models.protagonist import protag, protag_response
from src.environment.instance import env
from src.utils.mapper import protagonist_mapping

app, ns = server.app, server.ns

class ProtagMapper(object):
    def __init__(self):
        pass

    def search_property_batch(self, protagonist, limit):
        pl = protagonist_mapping(protagonist, limit, server.w2v_model)
        return {"results": pl}

pm = ProtagMapper()

@ns.route('/entity/protagonist')
class ProtagonistMapper(Resource):
    @ns.expect(protag, validate=True)
    @ns.marshal_list_with(protag_response)
    @ns.doc(params={
        'item': 'String you want to map to Wikidata Entity', 
        'limit': 'Limit entity candidates'
        })
    def post(self):
        return pm.search_property_batch(ns.payload['item'], ns.payload['limit'])
