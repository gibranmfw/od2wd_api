import json
from SPARQLWrapper import SPARQLWrapper, JSON

def dump_property(filename='property.json', path_to_save='resource/dump/'):
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql", agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11")

    sparql.setQuery("""
    SELECT ?property ?propertyLabel ?propertyDescription ?altLabel ?type 
        WHERE {
        ?property a wikibase:Property .
        MINUS { ?property wdt:P31 wd:Q18644427 }
        ?property wikibase:propertyType ?type .
        OPTIONAL { ?property skos:altLabel ?altLabel . FILTER (lang(?altLabel) = "id") }
        SERVICE wikibase:label { bd:serviceParam wikibase:language "id" }   
        } ORDER BY ASC(xsd:integer(strafter(str(?property), concat(str(wd:), "P"))))
    """)
    sparql.setReturnFormat(JSON)
    resultsId = sparql.query().convert()

    sparql.setQuery("""
    SELECT ?property ?propertyLabel ?propertyDescription ?altLabel
        WHERE {
        ?property a wikibase:Property .
        MINUS { ?property wdt:P31 wd:Q18644427 }
        OPTIONAL { ?property skos:altLabel ?altLabel . FILTER (lang(?altLabel) = "en") }
        SERVICE wikibase:label { bd:serviceParam wikibase:language "en" }   
        } ORDER BY ASC(xsd:integer(strafter(str(?property), concat(str(wd:), "P"))))
    """)
    sparql.setReturnFormat(JSON)
    resultsEn = sparql.query().convert()

    prop_list = {}
    id_stack = []
    alt_list = []
    dt = ''
    label = ''
    desc = ''
    for elem in resultsId['results']['bindings']:
        idp = elem['property']['value'].split('/')[4]
        if(idp not in id_stack):
            if(len(id_stack) == 0):
                id_stack.append(idp)
                dt = elem['type']['value'].split('#')[1]
                label = elem['propertyLabel']['value']
                if('propertyDescription' in elem):
                    desc = elem['propertyDescription']['value']
            else:
                alt_list.append(label)
                prop = {}
                prop['labelId'] = label
                prop['id'] = id_stack.pop()
                prop['aliasId'] = alt_list
                prop['descriptionId'] = desc
                if(dt == 'Monolingualtext' or dt == 'ExternalId'):
                    dt = 'String'
                prop['data type'] = dt
                
                
                prop_list[prop['id']] = prop
                alt_list = []
                if('altLabel' in elem):
                    alt_list.append(elem['altLabel']['value'])
                desc = ""
                
                id_stack.append(idp)
                dt = elem['type']['value'].split('#')[1]
                label = elem['propertyLabel']['value']
                if('propertyDescription' in elem):
                    desc = elem['propertyDescription']['value']
                
        else:
            alt_list.append(elem['altLabel']['value'])

    id_stack = []
    alt_list = []
    dt = ''
    label = ''
    desc = ''
    for elem in resultsEn['results']['bindings']:
        idp = elem['property']['value'].split('/')[4]
        if(idp not in id_stack):
            if(len(id_stack) == 0):
                id_stack.append(idp)
                label = elem['propertyLabel']['value']
                if('propertyDescription' in elem):
                    desc = elem['propertyDescription']['value']
            else:
                ids = id_stack.pop()
                alt_list.append(label)
                prop_list[ids]['labelEn'] = label
                prop_list[ids]['aliasEn'] = alt_list
                prop_list[ids]['descriptionEn'] = desc
                
                alt_list = []
                if('altLabel' in elem):
                    alt_list.append(elem['altLabel']['value'])
                desc = ""
                
                id_stack.append(idp)
                label = elem['propertyLabel']['value']
                if('propertyDescription' in elem):
                    desc = elem['propertyDescription']['value']
                
        else:
            alt_list.append(elem['altLabel']['value'])

    with open(path_to_save + filename, 'w') as outfile:
        json.dump(list(prop_list.values()), outfile)
        print("Finished dumping property at : data/dump/{}".format(filename))
