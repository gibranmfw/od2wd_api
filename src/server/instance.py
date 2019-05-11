import logging
import click
from flask import Flask
from flask_restplus import Api, Resource, fields

from gensim.models import Word2Vec

from src.environment.instance import environment_config, env
from src.utils.indexer import connect_elasticsearch

class ReverseProxied(object):
    '''Wrap the application in this middleware and configure the 
    front-end server to add these headers, to let you quietly bind 
    this to a URL other than / and to an HTTP scheme that is 
    different than what is used locally.

    In nginx:
    location /myprefix {
        proxy_pass http://192.168.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Scheme $scheme;
        proxy_set_header X-Script-Name /myprefix;
        }

    :param app: the WSGI application
    '''
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        script_name = environ.get('HTTP_X_SCRIPT_NAME', '')
        if script_name:
            environ['SCRIPT_NAME'] = script_name
            path_info = environ['PATH_INFO']
            if path_info.startswith(script_name):
                environ['PATH_INFO'] = path_info[len(script_name):]

        scheme = environ.get('HTTP_X_SCHEME', '')
        if scheme:
            environ['wsgi.url_scheme'] = scheme
        return self.app(environ, start_response)

class Server(object):
    def __init__(self):
        logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
        logging.root.setLevel(level=logging.INFO)
        logging.basicConfig(level=logging.ERROR)
        logger = logging.getLogger(__name__)
        self._logger = logger

        self.app = Flask(__name__)
        self.app.wsgi_app = ReverseProxied(self.app.wsgi_app)
<<<<<<< HEAD
        self.api = Api(self.app, 
            version='0.1', 
=======
        self.api = Api(self.app,
            version='0.1',
>>>>>>> 267c126053e04e7787e23cf3202ac77304cc60e9
            title='OD2WD API',
            description='Mapping Open Data to Wikidata', 
#            doc = environment_config["swagger-url"]
        )

        self.ns = self.api.namespace('main')
<<<<<<< HEAD
        self.load_logger()
        self.load_index()
        self.load_model()
    
=======
        self.es = connect_elasticsearch()
        self.w2v_model = Word2Vec.load(env['MODEL_PATH'] + env['MODEL_NAME'])

>>>>>>> 267c126053e04e7787e23cf3202ac77304cc60e9
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
<<<<<<< HEAD
=======

#@server.app.before_first_request
#def setup():
#    server.load_logger()
#    server.load_index()
#    server.load_model()
>>>>>>> 267c126053e04e7787e23cf3202ac77304cc60e9
