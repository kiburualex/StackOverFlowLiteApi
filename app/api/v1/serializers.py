from flask_restplus import fields
from app.api.v1 import api

question = api.model('Question', {
    'id': fields.Integer(readOnly=True, description='The question unique identifier'),
    'title': fields.String(required=False, description='The title of tehe Question'),
    'description': fields.String(required=False, description='The question details'),
    'user': fields.String(required=False, description='The name of the user'),
    'answers': fields.List(required=False, cls_or_instance=fields.Raw)
})

answer = api.model('Answer', {
    'id': fields.Integer(readOnly=False, description='The question unique identifier'),
    'answer': fields.String(required=False, description='The answer given'),
    'user': fields.String(required=False, description='The name of the user')
})


user = api.model('User', {
    'id': fields.Integer(readOnly=False, description='The user unique identifier'),
    'name': fields.String(required=False, description='The name of the user'),
    'email': fields.String(required=False, description='The email details'),
    'password': fields.String(required=False, description='The password details')
})
