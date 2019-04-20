import logging
import click
from flask import Flask
from flask_restplus import Api, Resource, fields

from gensim.models import Word2Vec

from src.environment.instance import environment_config, env
from src.utils.indexer import connect_elasticsearch

class Server(object):
    def __init__(self):
        self.app = Flask(__name__)
        self.api = Api(self.app, 
            version='0.1', 
            title='OD2WD API',
            description='Mapping Open Data to Wikidata', 
            doc = environment_config["swagger-url"]
        )

        self.ns = self.api.namespace('main')
    
    def load_model(self):
        self.w2v_model = Word2Vec.load(env['MODEL_PATH'] + env['MODEL_NAME'])

    def load_logger(self):
        logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
        logging.root.setLevel(level=logging.INFO)
        logging.basicConfig(level=logging.ERROR)
        logger = logging.getLogger(__name__)
        self._logger = logger
    
    def load_index(self):
        self.es = connect_elasticsearch()

    def run(self):
        self.app.run(
                debug = environment_config["debug"], 
                port = environment_config["port"]
            )

server = Server()

@server.app.before_first_request
def setup():
    server.load_logger()
    server.load_index()
    server.load_model()