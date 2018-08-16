from flask_restplus import fields
from app.api.v1 import api

question = api.model('Question', {
    'id': fields.Integer(readOnly=True, description='The question unique identifier'),
    'title': fields.String(required=True, description='The title of tehe Question'),
    'description': fields.String(required=True, description='The question details'),
    'answers': fields.List(cls_or_instance=fields.Raw)
})

user = api.model('User', {
    'id': fields.Integer(readOnly=True, description='The user unique identifier'),
    'name': fields.String(required=True, description='The name of the user'),
    'email': fields.String(required=True, description='The email details'),
    'password': fields.String(required=True, description='The password details')
})