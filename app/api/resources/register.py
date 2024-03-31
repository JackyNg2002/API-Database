import uuid

from flask_restful import Resource, reqparse
from werkzeug.security import generate_password_hash

from ..models.user import UserModel
from ..common.utils import res
from ..schema.register_sha import reg_args_valid


class Register(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        reg_args_valid(parser)
        data = parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return res(data=None, message="User {} already exists".format(data['username']), code=-1, status=400)
        else:
            try:
                data['salt']=uuid.uuid4().hex
                data['pwd'] = generate_password_hash('{}{}'.format(data['salt'], data['pwd']))
                user = UserModel(**data)
                user.add_user()
                return res(data=None, message="User {} created successfully".format(data['username']), code=0, status=200)
            except Exception as e:
                return res(data=None, message="An error occurred while creating the user", code=-1, status=500)
