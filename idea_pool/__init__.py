import secrets
from idea_pool.user.user_model import User
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from idea_pool.db_api import close_connection, init_db


app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'super-secret'
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

api = Api(app)
jwt = JWTManager(app)
init_db(app)


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return User.get_revoked_token(jti) is not None

@app.teardown_appcontext
def suhtdown(exception):
    close_connection()

from idea_pool.user import user_resources 
from idea_pool.idea import idea_resources

api.add_resource(user_resources.UserSignup, '/users')
api.add_resource(user_resources.AccessTokens, '/access-tokens')
api.add_resource(user_resources.RefreshTokens, '/access-tokens/refresh')
api.add_resource(user_resources.CurrentUser, '/me')
api.add_resource(idea_resources.Ideas, '/ideas', '/ideas/<idea_id>')