from flask_restplus import fields
from src.server.instance import server

nerInput = server.api.model('NER Input', {
    'title': fields.String(required=True, min_length=1, description='Title of the data', example='Data Sekolah Rawan Banjir di Jakarta'),
})

nerResponse = server.api.model('NER response', {
    "results": fields.List(fields.String(required=True, min_length=1, description='Entities in the Title', example='Jakarta'))
})
