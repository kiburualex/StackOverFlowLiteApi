import logging

from flask_restplus import Resource
from app.api.v1 import api
from app.api.v1.serializers import user
from app.user.models import User

log = logging.getLogger(__name__)

ns = api.namespace('api/v1/users', description='Operations related to Users')

UserMaker = User(api)


@ns.route('/')
class UsersList(Resource):
    """Shows a list of all users, and lets you POST to add new user"""

    @ns.doc('list_users')
    @ns.marshal_list_with(user)
    def get(self):
        """List all users"""
        return UserMaker.users

    @ns.doc('create_user')
    @ns.expect(user)
    @ns.marshal_with(user, code=201)
    def post(self):
        """Create a new user"""
        return UserMaker.create(api.payload), 201


@ns.route('/<int:id>')
@ns.response(404, 'User not found')
@ns.param('id', 'The user identifier')
class User(Resource):
    """Show a single user item and lets you delete them"""

    @ns.doc('get_user')
    @ns.marshal_with(user)
    def get(self, id):
        """Fetch a given resource"""
        return UserMaker.get(id)

    @ns.doc('delete_user')
    @ns.response(204, 'User deleted')
    def delete(self, id):
        """Delete a user given its identifier"""
        UserMaker.delete(id)
        return '', 204

    @ns.expect(user)
    @ns.marshal_with(user)
    def put(self, id):
        """Update a user given its identifier"""
        return UserMaker.update(id, api.payload)
