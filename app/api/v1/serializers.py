from flask_restplus import fields
from app.api.v1 import api

question_model = api.model('Question', {
    'id': fields.Integer(readOnly=True, description='The question unique identifier'),
    'title': fields.String(required=False, description='The title of the Question'),
    'description': fields.String(required=False, description='The question details'),
    'user_id': fields.Integer(required=False, description='The id of the user')
})

answer_model = api.model('Answer', {
    'id': fields.Integer(description='The question unique identifier'),
    'user_id': fields.Integer(description='The id of the user'),
    'question_id': fields.Integer(description='The id of the question'),
    'description': fields.String(description='The description of the answer'),
    'accepted': fields.Boolean(description='The status of the answers (if accepted as the right answer')
})


user_model = api.model('User', {
    'id': fields.Integer(description='The user unique identifier'),
    'username': fields.String(description='The name of the user'),
    'email': fields.String(description='The email details'),
    'role': fields.String(description='The role details'),
    'password': fields.String(description='The password details')
})
