import requests
import json
import urllib
from SPARQLWrapper import SPARQLWrapper, JSON

def searchEntity(keyword, limit):
    keyword = urllib.parse.quote(keyword)
    url = "https://www.wikidata.org/w/api.php?action=wbsearchentities&search={}&limit={}&language=id&format=json".format(keyword,limit)
    res = requests.get(url)
    return json.loads(res.text)

def searchObjWProperty(subject_id, property_id):
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

    sparql.setQuery("""
    SELECT ?item ?itemLabel ?grandItem ?grandItemLabel
    WHERE
    {
      bind (wd:%s as ?entity)
      wd:%s wdt:%s ?item .
      ?item wdt:P279 ?grandItem
      MINUS { ?entity wdt:P31 wd:Q4167410 }
      SERVICE wikibase:label { bd:serviceParam wikibase:language "id" }
    }
    """ % (subject_id, subject_id, property_id))
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results

def searchSbjWProperty(object_id, property_id):
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

    sparql.setQuery("""
    SELECT ?item ?itemLabel
    WHERE
    {
        ?item wdt:%s wd:%s .
        SERVICE wikibase:label { bd:serviceParam wikibase:language "id" }
    }
    """ % (property_id, object_id))
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results

def searchProperty(subject_id, object_id):
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

    sparql.setQuery("""
    SELECT ?item ?itemLabel
    WHERE
    {
        wd:%s ?item wd:%s .
        SERVICE wikibase:label { bd:serviceParam wikibase:language "id" }
    }
    """ % (subject_id, object_id))
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results

def searchPropertyRange(property_id):
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

    sparql.setQuery("""
    #Subproperties of location (P276)
    SELECT ?wbtype 
    WHERE {
    wd:%s wikibase:propertyType  ?wbtype.
    SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
    }
    """ % (property_id))
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results

def is_class(entity_id):
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

    sparql.setQuery("""
    SELECT distinct ?protag  WHERE { 
        bind (wd:%s as ?protag)
        ?x wdt:P31 ?protag
    }
    """% (entity_id))
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return len(results['results']['bindings']) > 0

def is_instance_of(entity_id, class_id):
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

    sparql.setQuery("""
    SELECT ?item ?itemLabel
    WHERE
    {
        bind (wd:%s as ?item)
        wd:%s wdt:P31 ?item .
        SERVICE wikibase:label { bd:serviceParam wikibase:language "id" }
    }
    """% (class_id, entity_id))
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return len(results['results']['bindings']) > 0
