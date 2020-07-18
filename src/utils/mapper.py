import logging
import json
import numpy as np
import re

from itertools import islice
from collections import OrderedDict
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

from src.utils.indexer import search
from src.utils.wikimedia import searchEntity, searchObjWProperty, searchProperty, is_class, is_instance_of, searchEntityWikidata, searchEntityWikimedia, getEntityData, get_labels

def preprocessing(text, option=None):
    if(option == 'property'):
        factory = StopWordRemoverFactory()
        stopword = factory.create_stop_word_remover()
        text = re.sub("([\(\[]).*?([\)\]])", "\g<1>\g<2>", text)
        text = stopword.remove(text)

    elif(option == 'protagonist'):
        text = text.replace('_', ' ')
        if(' ' in text):
            protag_list = text.split(' ')
            text = ' '.join(protag_list[1:len(protag_list)])
        if('/' in text):
            protag_list = text.split('/')
            text = protag_list[0]

    text = text.replace('_', ' ')
    text = text.replace('(', '')
    text = text.replace(')', '')
    text = text.replace(',', ' ')
    text = text.replace('&', ' ')
    text = text.lower()

    return text
    
def sigmoid(x, derivative=False):
    sigm = 1. / (1. + np.exp(-x))
    if derivative:
        return sigm * (1. - sigm)
    return sigm

def transform_sigmoid(nums):
    return sigmoid(nums, True) / 0.25

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

def ranking(candidateList, property_data, model, is_protagonist=False):
    res = []
    for candidate in candidateList:
        if(is_protagonist):
            if(is_instance_of(candidate['id'], property_data)):
                res.append({'candidate': candidate, 'score': 1})
            else:
                res.append({'candidate': candidate, 'score': 0})
        else:
            results = searchObjWProperty(candidate['id'], 'P31')
            sim = 0
            if(len(results['results']['bindings']) <= 0):
                results = searchObjWProperty(candidate['id'], 'P279')
                if(len(results['results']['bindings']) <= 0):
                    if('description' in candidate and candidate['description'] == 'Wikimedia disambiguation page'):
                        continue
                    res.append({'candidate': candidate, 'score': 0})
                    continue
                    
            candVector = phrase_vector(model, property_data)
            if(candVector is not None):
                for parent in results['results']['bindings']:
                    parVector = phrase_vector(model, preprocessing(parent['itemLabel']['value']))
                    gpVector = phrase_vector(model, preprocessing(parent['grandItemLabel']['value']))
                    temp = 0
                    if(parVector is not None):
                        temp = cosine_sim(candVector, parVector)
                    if(gpVector is not None):
                        temp2 = cosine_sim(candVector, gpVector)
                        temp = temp if temp > temp2 else temp2 
                    sim = sim if sim > temp else temp
            
            if(sim <= 0.2):
                sim = 0
            res.append({'candidate': candidate, 'score': sim})
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
            if(lwords[n].isnumeric()):
                continue
            lword_vector = lword_vector + model[lwords[n]]
    except KeyError:
        lword_vector = None
    finally:
        return lword_vector

def cosine_sim(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1)* np.linalg.norm(v2))

def getEntityCandidate(keyword, context, limit=5):
    entities = searchEntityWikimedia(keyword, context, limit)
    res = []
    for entity in entities:
        resultEntity = getEntityData(entity['title'])
        if (len(resultEntity) > 0):
            resultEntity = resultEntity[0]
            description = resultEntity['entityDescription']['value'] if 'entityDescription' in resultEntity else ''
            label = resultEntity['label']['value'] if 'label' in resultEntity else ''
            res.append({
                'id': resultEntity['entity']['value'].split('/')[4],
                'label': label,
                'description': description
            })
    return res

def checkProperty(model, entityId, columnValue):
    results = searchObjWProperty(entityId, 'P31')
    sim = 0
    if(len(results['results']['bindings']) <= 0):
        results = searchObjWProperty(entityId, 'P279')
        if(len(results['results']['bindings']) <= 0):
            return 0
    candVector = phrase_vector(model, columnValue)
    if(candVector is not None):
        for parent in results['results']['bindings']:
            parVector = phrase_vector(model, preprocessing(parent['itemLabel']['value']))
            gpVector = phrase_vector(model, preprocessing(parent['grandItemLabel']['value']))
            temp = 0
            if(parVector is not None):
                temp = cosine_sim(candVector, parVector)
            if(gpVector is not None):
                temp2 = cosine_sim(candVector, gpVector)
                temp = temp if temp > temp2 else temp2 
            sim = sim if sim > temp else temp

    return sim

def checkEntity(model, keyword, entityId):
    entityVector = phrase_vector(model, keyword)
    sim = 0
    if (entityVector is not None):
        labels = get_labels(entityId)
        for label in labels:
            cleanLabel = preprocessing(label)
            labelVector = phrase_vector(model, cleanLabel)
            temp = 0
            if (labelVector is not None):
                temp = cosine_sim(entityVector, labelVector)
            sim = sim if sim > temp else temp
    return sim

def mapEntity(model, keyword, columnValue, context, limit=5):
    clean_keyword = preprocessing(keyword)
    entities = getEntityCandidate(clean_keyword, context, limit)
    if (len(entities) < 1):
        print('{} score: 0'.format(keyword))
        return {'label': 'NOT FOUND', 'id': 'NOT FOUND'}
    entity = entities[0]
    if('description' in entity and entity['description'] == 'Wikimedia disambiguation page'):
        return None
    initialScore = checkProperty(model, entity['id'], columnValue)
    entityScore = checkEntity(model, clean_keyword, entity['id'])
    finalScore = (initialScore + entityScore) / 2
    # print('{} score: {}'.format(keyword, finalScore))
    if (finalScore > 0.3):
        entity['score'] = finalScore
        return entity
    else:
        return {'label': 'NOT FOUND', 'id': 'NOT FOUND', 'description': 'NOT FOUND', 'score': 0}
    
def map_entity_batch(datas, model):
    res_list = []
    for data in datas:
        res_map = {}
        contexts = data['contexts']
        contexts.append(data['headerValue'])
        res_map = {}
        # model, keyword, columnValue, context, limit=5
        el = mapEntity(model, data['item'], data['headerValue'], contexts, data['limit'])
        res = {"id": el['id'], "label": el['label'], "description": el['description'], 'score': el['score']}
        res_map['item'] = res
        res_list.append(res_map)
    return res_list

def map_property(header, header_range, property_index, w2v_model, es_client, limit):
    header = preprocessing(header, 'property')
    result = {}
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
        qword_vector = phrase_vector(w2v_model, header)
        for item in res:
            alias_vector = []
            sim = 0
            alias = item['_source']['aliasId']
            if(qword_vector is not None):
                for alt  in alias:
                    alt = preprocessing(alt)
                    temp = phrase_vector(w2v_model, alt)
                    if(temp is not None):
                        alias_vector.append(temp)

                sim = best_sim_score(alias_vector, qword_vector)

            pattern = re.compile("^(P[0-9]+)+$")
            lbl = ''
            if(pattern.match(item['_source']['labelId'])):
                lbl = item['_source']['labelEn']
            else:
                lbl = item['_source']['labelId']

            result[min(sim, 1.0)] = {
                'id': item['_source']['id'], 
                'label': lbl,
                'description': item['_source']['descriptionEn']
                }
    
    od = OrderedDict(sorted(result.items(), reverse=True))

    return OrderedDict(islice(od.items(), 0, limit))


def map_property_batch(properties, property_index, w2v_model, es_client):
    res_list = []
    for prop in properties:
        res_map = {}
        cand_list = []
        cand_props = map_property(prop['item'], prop['item_range'], property_index, w2v_model, es_client, prop['limit'])
        for key, value in cand_props.items():
            res = {"id": value['id'], "label": value['label'], "description": value['description'], "score": key}
            cand_list.append(res)
        res_map['item'] = prop['item']
        res_map['map_to'] = cand_list
        res_list.append(res_map)
    return res_list

def protagonist_mapping(protagonist, limit, w2v_model):
    protagonist = preprocessing(protagonist, 'protagonist')
    jsons = searchEntity(protagonist, limit)['search']
    qword_vector = phrase_vector(w2v_model, protagonist)
    result = {}
    if(qword_vector is not None):
        for json in jsons:
            # if(json['candidate']['match']['language'] != 'id'):
            #     continue
            ids = json['id']
            if(is_class(ids)):
                alias = []
                if('aliases' in json.keys()):
                    alias = json['aliases']
                label = json['match']['text']
                if(label not in alias):
                    alias.append(label)

                description = ''
                if('description' in json.keys()):
                    description = json['description']
            
                sim = 0
                alias_vector = []
                for alt in alias:
                    alt = preprocessing(alt)
                    temp = phrase_vector(w2v_model, alt)
                    if(temp is not None):
                        alias_vector.append(temp)
                        
                sim = best_sim_score(alias_vector, qword_vector)
                protag_map = {'id': ids, 'label': alias[0], 'description': description}
                if(sim in result.keys()):
                    result[sim].append(protag_map)
                else:
                    result[sim] = [protag_map]
    else:
        for json in jsons:
            if(json['match']['language'] != 'id'):
                continue
            ids = json['id']
            if(is_class(ids)):
                alias = []
                if('aliases' in json.keys()):
                    alias = json['aliases']
                label = json['match']['text']
                if(label not in alias):
                    alias.append(label)

                description = ''
                if('description' in json.keys()):
                    description = json['description']
                
                dist = 0
                for alt in alias:
                    alt = preprocessing(alt)
                    dist = lDistance(alt, protagonist)
                    if(dist <= 3):
                        score = transform_sigmoid(dist)
                        protag_map = {'id': ids, 'label': alias[0], 'description': description}
                        if(score in protag_map.keys()):
                            result[score].append(protag_map)
                        else:
                            result[score] = protag_map
                        
    if(len(result) == 0):
        result[0] = [{'id': 'NOT FOUND', 'label':'NOT FOUND', 'description': 'NOT FOUND'}]
    else:
        result = OrderedDict(sorted(result.items(), reverse=True))
        result = OrderedDict(islice(result.items(), 0, limit))
    
    cand_list = []
    for key, values in result.items():
        for value in values:
            res = {"id": value['id'], "label": value['label'], "description": value['description'], "score": key}
            cand_list.append(res)
    return cand_list
