import logging

from flask_restplus import Resource
from app.api.v1 import api
from app.api.v1.serializers import answer_model
from app.modules.answer.models import Answer
from app.utils.token_decorator import token_required
from .question import ns

log = logging.getLogger(__name__)

@ns.route('/<int:id>/answers')
@ns.param('id', 'The question Id')
class AnswerMethods(Resource):

    @token_required
    @api.marshal_with(answer_model, as_list=True)
    def get(self, id):

        """Fetch a given question\'s answers """
        return Answer({"question_id":id}).fetch_all(), 200

    @token_required
    @ns.marshal_with(answer_model, code=201)
    def post(self, id):

        """Create a new answer"""
        api.payload["question_id"] = id
        return Answer(api.payload).save(), 201


@ns.route('/<int:question_id>/answers/<int:id>')
@ns.param('question_id', 'The Question Id')
@ns.param('id', 'The Answer Id')
class AnswerDetails(Resource):

    @token_required
    @ns.marshal_with(answer_model)
    def get(self, question_id, id):

        """Fetch a given question\'s answers """

        return Answer({"answer_id": id}).get_by_id()

    @token_required
    @ns.response(202, 'Answer deleted')
    def delete(self,question_id, id):

        """Delete a question given its identifier"""

        return Answer({"answer_id": id}).delete(), 202

    @token_required
    @ns.expect(answer_model)
    @ns.marshal_with(answer_model)
    def put(self, question_id, id):

        """Update a question given its identifier"""
        api.payload["question_id"] = question_id
        api.payload["answer_id"] = id

        return Answer(api.payload).update()
