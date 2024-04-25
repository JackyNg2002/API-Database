import os

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from .config import config
from .api.models import db

from .api.models.user import UserModel
from .api.models.revoked_token import RevokedTokenModel
from .api.models.robot import RobotModel
from .api.models.record import RecordModel
from .api.models.map import MapModel
from .api.models.permission import PermissionModel


from .manage import migrate

from .api import api_blueprint


def create_app(config_name):
    static_folder = os.path.abspath(os.path.join(os.path.dirname(__file__),'..',config[config_name].DATA_STORAGE_PATH) )
    app = Flask(__name__,static_folder=static_folder)
    app.config.from_object(config[config_name])
    db.init_app(app)

    migrate.init_app(app, db, render_as_batch=True)
    jwt = JWTManager(app)
    registerJwtHooks(jwt)

    app.register_blueprint(api_blueprint)
    CORS(app)
    
    # use for testing
    # from flask_restful import Resource,Api
    # api=Api(app)
    # class HelloWorld(Resource):
    #     def get(self):
    #         return {'hello': 'world'}

    # api.add_resource(HelloWorld, '/')


    return app

def registerJwtHooks(jwt):
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header,decrypted_token):
        jti = decrypted_token['jti']
        return RevokedTokenModel.is_jti_blacklisted(jti)
    @jwt.expired_token_loader
    def expired_token_loader(jwt_header,jwt_data):
        return {
            'msg': 'expired token ',
            'error': 'expired token required',
            'code': '7777'
        }, 200
    @jwt.revoked_token_loader
    def revoked_token_loader(jwt_header,jwt_data):
        return {
            'msg': 'Invalid token',
            'error': 'invalid_token',
            'code': '7777'
        }, 200
    @jwt.invalid_token_loader
    def invalid_token_loader(jwt_header,jwt_data):
        return {
            'msg': 'Invalid token',
            'error': 'invalid_token',
            'code': '7777'
        }, 200
    @jwt.unauthorized_loader
    def unauthorized_loader(jwt_header,jwt_data):
        return {
            'msg': 'Invalid token',
            'error': 'invalid_token',
            'code': '7777'
        }, 200


app = create_app(os.getenv('FLASK_ENV') or 'default')