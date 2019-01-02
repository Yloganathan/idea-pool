from flask_restful import Resource, reqparse
from .user_model import User
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from werkzeug.security import safe_str_cmp

class UserSignup(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', help = 'Email field cannot be blank', required = True)
        parser.add_argument('name', help = 'Name field cannot be blank', required = True)
        parser.add_argument('password', help = 'Password field cannot be blank', required = True)

        data = parser.parse_args()
        
        if User.find_by_email(data['email']):
            return {'msg': 'User {} already exists'.format(data['name'])}, 400
        
        new_user = User(
            email = data['email'],
            name = data['name'],
            password = data['password'].encode('utf-8')
        )
        
        try:
            User.create(new_user)
            access_token = create_access_token(identity = data['email'])
            refresh_token = create_refresh_token(identity = data['email'])
            return {
                'jwt': access_token,
                'refresh_token': refresh_token
                }
        except:
            return {'msg': 'Something went wrong'}, 500


class AccessTokens(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', help = 'Email field cannot be blank', required = True)
        parser.add_argument('password', help = 'Password field cannot be blank', required = True)

        data = parser.parse_args()

        user = User.find_by_email(data['email'])

        if not user:
            return {'msg': 'User {} doesn\'t exist'.format(data['email'])}, 400
        
        if safe_str_cmp(user['password'], data['password'].encode('utf-8')):
            access_token = create_access_token(identity = data['email'])
            refresh_token = create_refresh_token(identity = data['email'])
            return {
                'jwt': access_token,
                'refresh_token': refresh_token
                }
        else:
            return {'msg': 'Wrong credentials'}, 400

    @jwt_required
    def delete(self):
        jti = get_raw_jwt()['jti']
        User.revoke_token(jti)
        return {}, 204


class RefreshTokens(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity = current_user)
        return {'jwt': access_token}


class CurrentUser(Resource):
    @jwt_required
    def get(self):
        current_user = get_jwt_identity()
        user = User.find_by_email(current_user)
        user.pop('password')
        return user

