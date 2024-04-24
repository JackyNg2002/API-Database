from flask import Blueprint
from flask_restful import Api

from .resources.auth.register import Register
from .resources.auth.login import Login
from .resources.auth.user import User
from .resources.auth.logout import Logout

from .resources.user import UserService
from .resources.map import MapService
from .resources.record import RecordService
from .resources.permission import PermissionService
from .resources.robot import RobotService

api_blueprint = Blueprint('api', __name__,url_prefix='/api')
api = Api(api_blueprint)

api.add_resource(Register, '/auth/register')
api.add_resource(Login, '/auth/login','/auth/refreshToken')
api.add_resource(User, '/auth/user')
api.add_resource(Logout, '/auth/logout')


api.add_resource(UserService, '/user')
api.add_resource(MapService, '/map')
api.add_resource(RecordService, '/record')
api.add_resource(PermissionService, '/permission')
api.add_resource(RobotService, '/robot')
