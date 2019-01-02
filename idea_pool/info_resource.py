from flask_restful import Resource
from flask import current_app

class Info(Resource):
    def get(self):
        INFO_FILE = 'version.txt'
        with current_app.open_resource(INFO_FILE, 'r') as f:
                version = f.read().strip()
        build = 'DEBUG' if current_app.debug else 'RELEASE'
        return {'build': build, 'version': version}
        