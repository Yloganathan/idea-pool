from flask_restful import Resource, reqparse
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from .idea_model import Idea
import secrets

class Ideas(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('content', help = 'content field cannot be blank', required = True)
    parser.add_argument('impact', help = 'impact field cannot be blank', required = True)
    parser.add_argument('ease', help = 'ease field cannot be blank', required = True)
    parser.add_argument('confidence', help = 'confidence field cannot be blank', required = True)

    @jwt_required
    def get(self):
        current_user = get_jwt_identity()
        return Idea.get_by_user(current_user)

    @jwt_required
    def post(self):
        current_user = get_jwt_identity()
        data = Ideas.parser.parse_args()
        new_idea = Idea(
            email = current_user,
            id = secrets.token_hex(9),
            content = data['content'],
            impact = int(data['impact']),
            ease = int(data['ease']),
            confidence = int(data['confidence'])
        )

        return Idea.create(new_idea)

    @jwt_required
    def put(self, idea_id):
        data = Ideas.parser.parse_args()
        update_idea = Idea(
            id = idea_id,
            content = data['content'],
            impact = int(data['impact']),
            ease = int(data['ease']),
            confidence = int(data['confidence'])
        )
        return Idea.update(update_idea)

    @jwt_required
    def delete(self, idea_id):
        return Idea.delete(idea_id)