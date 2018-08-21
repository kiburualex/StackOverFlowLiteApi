import logging

from flask_restplus import Resource
from app.api.v1 import api
from app.api.v1.serializers import question, answer
from app.question.models import Question

log = logging.getLogger(__name__)

ns = api.namespace('api/v1/questions', description='Operations related to Questions')

QuestionMaker = Question(api)


@ns.route('/')
class QuestionList(Resource):
    """Shows a list of all questions, and lets you POST to add new question"""

    @ns.doc('list_questions')
    @ns.marshal_list_with(question)
    def get(self):
        """List all questions"""
        return QuestionMaker.questions

    @ns.doc('create_question')
    @ns.expect(question)
    @ns.marshal_with(question, code=201)
    def post(self):
        """Create a new question"""
        return QuestionMaker.create(api.payload), 201


@ns.route('/<int:id>')
@ns.response(404, 'Question not found')
@ns.param('id', 'The question identifier')
class Question(Resource):
    """Show a single question item and lets you delete them"""

    @ns.doc('get_question')
    @ns.marshal_with(question)
    def get(self, id):
        """Fetch a given resource"""
        return QuestionMaker.get(id)

    @ns.doc('delete_question')
    @ns.response(204, 'Question deleted')
    def delete(self, id):
        """Delete a question given its identifier"""
        QuestionMaker.delete(id)
        return '', 204

    @ns.expect(question)
    @ns.marshal_with(question)
    def put(self, id):
        """Update a question given its identifier"""
        return QuestionMaker.update(id, api.payload)


@ns.route('/<int:id>/answer')
@ns.response(404, 'Answer not found')
@ns.param('id', 'The question Id')
class QuestionAnswer(Resource):
    """Show a single question answer and lets you delete them"""

    @ns.doc('get_answer')
    @api.marshal_with(answer, as_list=True)
    def get(self, id):
        """Fetch a given question\'s answers """
        return QuestionMaker.get_answers(id), 200

    @ns.doc('create_answer')
    @ns.marshal_with(answer, code=201)
    def post(self, id):
        """Create a new answer"""
        return QuestionMaker.create_answer(id, api.payload), 201
