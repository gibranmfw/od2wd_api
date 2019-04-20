import os.path
import sys
import multiprocessing
from gensim.corpora import WikiCorpus
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence

def preprocessing(logger, data_path, output_filename):
    i = 0
    output = open(output_filename, 'w', encoding="utf-8")

    wiki = WikiCorpus(data_path, lemmatize=False, dictionary={}, lower=False)
    for text in wiki.get_texts():
        output.write(' '.join(text) + '\n')
        i = i + 1
        if i % 10000 == 0:
            logger.info("Saved " + str(i) + " articles")
    
    output.close()
    logger.info("Finished Saved " + str(i) + " articles")

def train_word2vec(logger, train_data, model_path):
    logger.info("Start Training")
    model = Word2Vec(LineSentence(train_data), size=400, window=5, min_count=5, workers=multiprocessing.cpu_count())
    
    # trim unneeded model memory = use (much) less RAM
    model.init_sims(replace=True)
    model.save(model_path)
    logger.info("Finished train model, saved in: " + model_path)