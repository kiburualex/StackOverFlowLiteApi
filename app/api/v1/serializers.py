from flask_restplus import fields
from app.api.v1 import api

""" Serialize the question model """

question_model = api.model('Question', {
    'id': fields.Integer(readOnly=True, description='The question unique identifier'),
    'user_id': fields.Integer(required=False, description='The id of the user'),
    'title': fields.String(required=False, description='The title of the Question'),
    'body': fields.String(required=False, description='The body of the Question')
})


""" Serialize the answer model """

answer_model = api.model('Answer', {
    'id': fields.Integer(description='The question unique identifier'),
    'user_id': fields.Integer(description='The id of the user'),
    'question_id': fields.Integer(description='The id of the question'),
    'answer_body': fields.String(description='The description of the answer'),
    'accepted': fields.Boolean(description='The status of the answers (if accepted as the right answer')
})


""" Serialize the User model """

user_model = api.model('User', {
    'id': fields.Integer(description='The user unique identifier'),
    'username': fields.String(description='The name of the user'),
    'email': fields.String(description='The email details'),
    'role': fields.String(description='The role details'),
    'password': fields.String(description='The password details')
})


""" Serialize the Authentication details from User model"""

auth_model = api.model('auth_details', {
    'email': fields.String(required=True, description='The email address'),
    'password': fields.String(required=True, description='The user password '),
})
