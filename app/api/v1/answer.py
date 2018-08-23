import logging

from flask_restplus import Resource
from app.api.v1 import api
from app.api.v1.serializers import answer_model
from app.modules.answer.models import Answer
from .question import ns

log = logging.getLogger(__name__)

@ns.route('/<int:id>/answers')
@ns.param('id', 'The question Id')
class AnswerMethods(Resource):
    @ns.doc('get_answer')
    @api.marshal_with(answer_model, as_list=True)
    def get(self, id):
        """Fetch a given question\'s answers """
        return Answer({"question_id":id}).fetch_all(), 200

    @ns.doc('create_answer')
    @ns.marshal_with(answer_model, code=201)
    def post(self, id):
        """Create a new answer"""
        api.payload["question_id"] = id
        return Answer(api.payload).save(), 201


@ns.route('/<int:question_id>/answers/<int:id>')
@ns.param('question_id', 'The Question Id')
@ns.param('id', 'The Answer Id')
class AnswerDetails(Resource):
    """Show a single question answer and lets you delete them"""

    @ns.doc('get_answer')
    @ns.marshal_with(answer_model)
    def get(self, question_id, id):
        """Fetch a given question\'s answers """
        return Answer({"answer_id": id}).get_by_id()

    @ns.doc('delete_answer')
    @ns.response(204, 'Answer deleted')
    def delete(self,question_id, id):
        """Delete a question given its identifier"""
        Answer({"answer_id": id}).delete()
        return '', 204

    @ns.doc('update_answer')
    @ns.expect(answer_model)
    @ns.marshal_with(answer_model)
    def put(self, question_id, id):
        """Update a question given its identifier"""
        api.payload["question_id"] = question_id
        api.payload["answer_id"] = id
        return Answer(api.payload).update_answer()
