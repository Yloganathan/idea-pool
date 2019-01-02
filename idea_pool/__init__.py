from idea_pool.user.user_model import User
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from idea_pool.db_api import close_connection, migrate_db
from idea_pool.user import user_resources 
from idea_pool.idea import idea_resources
from .info_resource import Info

def create_app(config='config.Config'):
    app = Flask(__name__)
    app.config.from_object(config)

    add_routes(app)
    add_auth(app)
    migrate_db(app)

    @app.teardown_appcontext
    def suhtdown(exception):
        close_connection()

    return app

def add_auth(app):
    jwt = JWTManager(app)

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        return User.get_revoked_token(jti) is not None

def add_routes(app):
    api = Api(app)
    api.add_resource(Info, '/')
    api.add_resource(user_resources.UserSignup, '/users')
    api.add_resource(user_resources.AccessTokens, '/access-tokens')
    api.add_resource(user_resources.RefreshTokens, '/access-tokens/refresh')
    api.add_resource(user_resources.CurrentUser, '/me')
    api.add_resource(idea_resources.Ideas, '/ideas', '/ideas/<idea_id>')