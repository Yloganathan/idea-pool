from flask_restful import Resource, reqparse
from flask import current_app
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from .idea_model import Idea
import secrets

class Ideas(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('content', help = 'content field cannot be blank', required = True)
    parser.add_argument('impact', help = 'impact field should be valid number between 1 and 10', type=int, required = True, choices=(1,2,3,4,5,6,7,8,9,10))
    parser.add_argument('ease', help = 'ease field should be valid number between 1 and 10', type=int, required = True, choices=(1,2,3,4,5,6,7,8,9,10))
    parser.add_argument('confidence', help = 'confidence field should be valid number between 1 and 10', type=int, required = True, choices=(1,2,3,4,5,6,7,8,9,10))
    
    @jwt_required
    def get(self):
        get_parser = reqparse.RequestParser()
        get_parser.add_argument('page', type=int, location='args')
        data = get_parser.parse_args()
        page = data['page'] or 1

        current_user = get_jwt_identity()
        all_ideas = Idea.get_by_user(current_user)

        page_size = current_app.config['PAGE_SIZE']
        start = (page - 1 ) * page_size
        end = page * page_size
        
        if start > len(all_ideas):
            return []
        
        if end > len(all_ideas):
            end = len(all_ideas)

        return all_ideas[start:end]


    @jwt_required
    def post(self):
        current_user = get_jwt_identity()
        data = Ideas.parser.parse_args()

        if len(data['content']) > 255 or len(data['content']) < 1:
            return {'msg': 'content should be between 1 to 255 char'}, 400

        new_idea = Idea(
            email = current_user,
            id = secrets.token_hex(9),
            **data
        )

        return Idea.create(new_idea)

    @jwt_required
    def put(self, idea_id):
        data = Ideas.parser.parse_args()

        idea = Idea.get_by_id(idea_id)

        if not idea:
            return {'msg': f'Idea with id {idea_id} doesn\'t exist'}, 400
        
        if len(data['content']) > 255 or len(data['content']) < 1:
            return {'msg': 'content should be between 1 to 255 char'}, 400
        
        update_idea = Idea( idea_id, **data)

        return Idea.update(update_idea)

    @jwt_required
    def delete(self, idea_id):
        idea = Idea.get_by_id(idea_id)

        if not idea:
            return {'msg': f'Idea with id {idea_id} doesn\'t exist'}, 400

        Idea.delete(idea_id)
        return {}, 204