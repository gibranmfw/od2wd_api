import logging
from flask import Flask
from flask_restplus import Api, Resource, fields

from gensim.models import Word2Vec

from environment.instance import environment_config, env
from utils.indexer import connect_elasticsearch

class Server(object):
    def __init__(self):
        logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
        logging.root.setLevel(level=logging.INFO)
        logging.basicConfig(level=logging.ERROR)
        logger = logging.getLogger(__name__)
        self._logger = logger

        self.app = Flask(__name__)
        self.api = Api(self.app, 
            version='0.1', 
            title='OD2WD API',
            description='Mapping Open Data to Wikidata', 
            doc = environment_config["swagger-url"]
        )

        self.ns = self.api.namespace('main')
    
        self.w2v_model = Word2Vec.load(env['MODEL_PATH'] + 'w2vec_wiki_id_case')
        self.es = connect_elasticsearch()
    def run(self):
        self.app.run(
                debug = environment_config["debug"], 
                port = environment_config["port"]
            )

server = Server()