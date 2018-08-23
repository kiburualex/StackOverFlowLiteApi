import logging

from flask_restplus import Resource
from app.api.v1 import api
from app.api.v1.serializers import user_model
from app.modules.user.models import User

log = logging.getLogger(__name__)

ns = api.namespace('api/v1/users', description='Operations related to Users')


@ns.route('/')
class UsersMethods(Resource):
    """Shows a list of all users, and lets you POST to add new user"""

    @ns.doc('list_users')
    @ns.marshal_list_with(user_model)
    def get(self):
        """List all users"""
        return User().fetch_all()

    @ns.doc('create_user')
    @ns.expect(user_model)
    @ns.marshal_with(user_model, code=201)
    def post(self):
        """Create a new user"""
        return User(api.payload).save(), 201


@ns.route('/<int:id>')
@ns.response(404, 'User not found')
@ns.param('id', 'The user identifier')
class UserDetail(Resource):
    """Show a single user item and lets you delete them"""

    @ns.doc('get_user')
    @ns.marshal_with(user_model)
    def get(self, id):
        """Fetch a given resource"""
        return User({"id": id}).get_by_id()

    @ns.doc('delete_user')
    @ns.response(204, 'User deleted')
    def delete(self, id):
        """Delete a user given its identifier"""
        User({"id": id}).delete()
        return '', 204

    @ns.expect(user_model)
    @ns.marshal_with(user_model)
    def put(self, id):
        """Update a user given its identifier"""
        return User(api.payload).update()
