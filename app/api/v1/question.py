import logging

from flask_restplus import Resource
from app.api.v1 import api
from app.api.v1.serializers import question_model
from app.modules.question.models import Question
from app.utils.token_decorator import token_required

log = logging.getLogger(__name__)

ns = api.namespace('api/v1/questions', description='Operations related to Questions')


@ns.route('/')
class QuestionsMethods(Resource):

    @token_required
    @ns.marshal_list_with(question_model)
    def get(self):

        """List all questions"""

        return Question().fetch_all()

    @token_required
    @ns.expect(question_model)
    @ns.marshal_with(question_model, code=201)
    def post(self):

        """Create a new question"""

        return Question(api.payload).save(), 201


@ns.route('/<int:id>')
@ns.response(404, 'Question not found')
@ns.param('id', 'The question identifier')
class QuestionDetail(Resource):

    @token_required
    @ns.marshal_with(question_model)
    def get(self, id):

        """Fetch a given resource"""

        return Question({"id": id}).get_by_id()

    @token_required
    @ns.response(202, 'Question deleted')
    def delete(self, id):

        """Delete a question given its identifier"""

        return Question({"id": id}).delete(), 202

    @token_required
    @ns.expect(question_model)
    @ns.marshal_with(question_model)
    def put(self, id):

        """Update a question given its identifier"""

        return Question(api.payload).update()
