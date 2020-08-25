import requests
import json
import urllib
from rdflib import Graph

def startNER(userInput):
    preprocessedUserInput = ' '.join(elem.capitalize() for elem in userInput.split())
    headers = {
        'Content-Type': 'application/x-turtle'
    }
    url = 'https://opentapioca.org/api/nif'
    payload = (
        "@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\r\n"
        "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\r\n"
        "@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\r\n"
        "@prefix nif: <http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#> .\r\n"
        "@prefix itsrdf: <http://www.w3.org/2005/11/its/rdf#> .\r\n\r\n"
        "<http://www.od2wd.id/evaluate/sentence-1>\r\n"
        " a nif:RFC5147String , nif:String , nif:Context ;\r\n"
        " nif:isString \"" + preprocessedUserInput + "\"@id ."
    )

    response = requests.post(url, headers=headers, data=payload)

    g = Graph()
    result = g.parse(data=response.text, format='turtle')
    res = []
    for _, p, o in result:
        if ("anchorOf" in p):
            res.append(o.toPython())
    return res