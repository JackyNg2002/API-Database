import os

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from .config import config
from .api.models import db
from .api.models.user import UserModel
from .api.models.revoked_token import RevokedTokenModel

from .manage import migrate

from .api import api_blueprint


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    db.init_app(app)

    migrate.init_app(app, db)
    jwt = JWTManager(app)
    registerJwtHooks(jwt)

    app.register_blueprint(api_blueprint)
    CORS(app)
    
    # use for testing
    from flask_restful import Resource,Api
    api=Api(app)
    class HelloWorld(Resource):
        def get(self):
            return {'hello': 'world'}

    api.add_resource(HelloWorld, '/')


    return app

def registerJwtHooks(jwt):
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blacklist(jwt_header,decrypted_token):
        jti = decrypted_token['jti']
        return RevokedTokenModel.is_jti_blacklisted(jti)

app = create_app(os.getenv('FLASK_ENV') or 'default')