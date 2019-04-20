# app/__init__.py

import json
import logging
import sys

# local import
from src.environment.instance import env
from src.utils.indexer import connect_elasticsearch, create_index, store_record, search
from src.utils.dumper import dump_property
from src.utils.word2vec import preprocessing, train_word2vec

logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
logging.root.setLevel(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_model(train_data="idwiki-latest-pages-articles.xml.bz2", model_name=env['MODEL_NAME']):
    logger.info("running %s" % ' '.join(sys.argv))
    preprocessing(logger, env['DUMP_PATH'] + train_data, env['DUMP_PATH'] + "wiki.id.case.text")
    train_word2vec(logger, env['DUMP_PATH'] + "wiki.id.case.text", env['MODEL_PATH'] + "w2vec_wiki_id_case")

def dumping_property(filename='property.json', path_to_save=env['DUMP_PATH']):
    logger.info('Start downloading wikidata property data')
    dump_property(filename, path_to_save)
    logger.info('Finish, data saved in: ' + path_to_save + filename)

def create_indexer(pi_name=env['PROPERTY_INDEX'], ei_name='wd_entity', prop_doc_type='members'):
    logger.info('Start creating Index')

    with open(env['DUMP_PATH'] + 'property.json') as f:
        prop_datas = json.load(f)

    es = connect_elasticsearch()
    if(create_index(es, pi_name) and create_index(es, ei_name)):
        logger.info("inputing data...")
        count = 0
        for elem in prop_datas:
            prop_data = json.dumps(elem)
            
            if(not store_record(es, pi_name, prop_data)):
                break
            else:
                count = count + 1

        logger.info("Finish creating index")
        logger.debug("Total data stored in index: {}".format(count))