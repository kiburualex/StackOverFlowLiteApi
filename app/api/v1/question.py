import logging

from flask_restplus import Resource
from app.api.v1 import api
from app.api.v1.serializers import question_model
from app.question.models import Question

log = logging.getLogger(__name__)

ns = api.namespace('api/v1/questions', description='Operations related to Questions')

question = Question(api)


@ns.route('/')
class Questions(Resource):
    """Shows a list of all questions, and lets you POST to add new question"""

    @ns.doc('list_questions')
    @ns.marshal_list_with(question_model)
    def get(self):
        """List all questions"""
        return question.fetch_all()

    @ns.doc('create_question')
    @ns.expect(question_model)
    @ns.marshal_with(question_model, code=201)
    def post(self):
        """Create a new question"""
        return question.create(api.payload), 201


@ns.route('/<int:id>')
@ns.response(404, 'Question not found')
@ns.param('id', 'The question identifier')
class QuestionDetail(Resource):
    """Show a single question item and lets you delete them"""

    @ns.doc('get_question')
    @ns.marshal_with(question_model)
    def get(self, id):
        """Fetch a given resource"""
        return question.get_question_by_id(id)

    @ns.doc('delete_question')
    @ns.response(204, 'Question deleted')
    def delete(self, id):
        """Delete a question given its identifier"""
        question.delete(id)
        return '', 204

    @ns.expect(question_model)
    @ns.marshal_with(question_model)
    def put(self, id):
        """Update a question given its identifier"""
        return question.update(id, api.payload)
