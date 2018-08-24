import logging
from flask import request
from flask_restplus import Resource
from app.api.v1 import api
from app.api.v1.serializers import auth_model, user_model
from app.modules.user.models import User
from app.utils.auth_helper import Auth

log = logging.getLogger(__name__)

ns = api.namespace('api/v1/auth', description='Operations related to Authentication')


@ns.route('/login')
class UserLogin(Resource):

    @api.doc('user login')
    @api.expect(auth_model, validate=True)
    def post(self):

        """ Login """
        post_data = request.json

        return Auth.login_user(data=post_data)


@ns.route('/logout')
class LogoutAPI(Resource):

    @api.doc('logout a user')
    def post(self):

        """ Logout """

        auth_header = request.headers.get('Authorization')

        return Auth.logout_user(data=auth_header)


@ns.route('/signup')
class UsersMethods(Resource):

    @ns.doc('create_user')
    @ns.expect(user_model)
    def post(self):

        """ Register a new user """

        return User(api.payload).register_new_user(), 201
