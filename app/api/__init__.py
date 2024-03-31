from flask import Blueprint
from flask_restful import Api

from .resources.auth.register import Register
from .resources.auth.login import Login
from .resources.auth.user import User
from .resources.auth.logout import Logout
from .resources.user import UserService

api_blueprint = Blueprint('api', __name__,url_prefix='/api')
api = Api(api_blueprint)

api.add_resource(Register, '/auth/register')
api.add_resource(Login, '/auth/login','/auth/refreshToken')
api.add_resource(User, '/auth/user')
api.add_resource(Logout, '/auth/logout')


api.add_resource(UserService, '/user')
