import logging
import json
import numpy as np

from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

from src.utils.indexer import search
from src.utils.wikimedia import searchEntity, searchObjWProperty, searchProperty

def lDistance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2+1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]

def ranking(candidateList, propertyLbl):
    res = []
    for i in range(len(candidateList)):
        results = searchObjWProperty(candidateList[i]['id'], 'P31')
        
        if(len(results['results']['bindings']) > 0):
            lblDis = lDistance(propertyLbl.lower(), results['results']['bindings'][0]['itemLabel']['value'].lower())   
            if(lblDis < 3):
                res.append(candidateList[i])
    
    if(len(res) == 0):
        res = candidateList

    return res

def best_sim_score(alias_vectors, query_vector):
    sim = 0
    for avec in alias_vectors:
        temp = cosine_sim(avec, query_vector)
        if(temp > sim):
            sim = temp
    return sim

def phrase_vector(model, word):
    lwords = word.lower().replace('/', ' ').split()
    try:
        lword_vector = model[lwords[0]]
        for n in range(1, len(lwords)):
            lword_vector = lword_vector + model[lwords[n]]
    except KeyError:
        lword_vector = None
    finally:
        return lword_vector

def cosine_sim(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1)* np.linalg.norm(v2))

def map_entity(data, context, model, limit=10):
    result = ''
    resultLabel = ''
    jsons = searchEntity(data.lower(), limit)['search']
    jsons = ranking(jsons, context)
    
    if(len(jsons) > 0):
        cand = None
        sim_score = -1
        qword_vector = phrase_vector(model, data)
        if(qword_vector is not None):
            for json in jsons:
                sim = 0
                
                elabel = json['label']
                eword_vector = phrase_vector(model, elabel)
                if(eword_vector is not None):
                    sim = cosine_sim(qword_vector, eword_vector)
                
                if(sim > sim_score):
                    sim_score = sim
                    cand = json
            
            result = cand['id']
            resultLabel = cand['label']
            
        else:
            result = 'NOT IN CORPUS'
            resultLabel = 'NOT IN CORPUS'
    else:
        result = 'NOT FOUND'
        resultLabel = 'NOT FOUND'
    
    return result, resultLabel

def map_entity_batch(datas, model, limit=10):
    res_list = []
    for data in datas:
        ids, label = map_entity(data['item'], data['context'], model, limit)
        res = {"id": ids, "label": label}
        res_list.append(res)
    return res_list

def map_property(header, header_range, property_index, w2v_model, es_client):
    factory = StopWordRemoverFactory()
    stopword = factory.create_stop_word_remover()

    header = header.replace('_', ' ')
    header2 = header.lower()
    header = stopword.remove(header2)

    result = ''
    resultLabel = ''

    search_object = {
            "from" : 0, 
            "size" : 100,
            "query": {
                "bool": {
                    "must": [
                        {
                            "term": {"data type": header_range}
                        },
                        {
                            "bool": {
                                "should": [
                                    {"match": {"aliasId": header}},
                                    {"match": {"aliasEn": header}}
                                ]
                            }
                        }
                    ]
                }
            }
        }
        
    res = search(es_client, property_index, json.dumps(search_object))['hits']['hits']
    if(len(res) > 0):
        cand = None
        sim_score = -1
        qword_vector = phrase_vector(w2v_model, header)
        for item in res:
            alias_vector = []
            sim = 0
            alias = item['_source']['aliasId']
            if(qword_vector is not None):
                for alt  in alias:
                    temp = phrase_vector(w2v_model, alt)
                    if(temp is not None):
                        alias_vector.append(temp)

                sim = best_sim_score(alias_vector, qword_vector)
            
            if(sim > sim_score):
                sim_score = sim
                cand = item
        
        result = cand['_source']['id']
        resultLabel = cand['_source']['labelId']
        
    return result, resultLabel


def map_property_batch(properties, property_index, w2v_model, es_client):
    res_list = []
    for prop in properties:
        ids, label = map_property(prop['item'], prop['item_range'], property_index, w2v_model, es_client)
        res = {"id": ids, "label": label}
        res_list.append(res)
    
    return res_list