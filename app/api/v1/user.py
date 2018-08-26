import logging

from flask_restplus import Resource
from app.api.v1 import api
from app.api.v1.serializers import user_model
from app.modules.user.models import User
from app.utils.token_decorator import token_required

log = logging.getLogger(__name__)

ns = api.namespace('api/v1/users', description='Operations related to Users')


@ns.route('/')
class UsersMethods(Resource):

    @token_required
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

    @token_required
    @ns.marshal_with(user_model)
    def get(self, id):

        """Fetch a given resource"""

        return User({"id": id}).get_by_id()

    @token_required
    @ns.response(202, 'User deleted')
    def delete(self, id):

        """Delete a user given its identifier"""

        return User({"id": id}).delete(), 202

    @token_required
    @ns.expect(user_model)
    @ns.marshal_with(user_model)
    def put(self, id):

        """Update a user given its identifier"""

        api.payload['id'] = id

        return User(api.payload).update()
