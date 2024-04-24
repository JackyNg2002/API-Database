import uuid
from flask_restful import Resource,reqparse
from flask_jwt_extended import jwt_required
from werkzeug.security import generate_password_hash
from ..models.user import UserModel
<<<<<<< HEAD
from ..models.permission import PermissionModel
=======
>>>>>>> 89f9055002e6d3439cf64c3e926889812a772e4f
from ..common.utils import res

class UserService(Resource):
    @jwt_required()
    def get(self):
        users = UserModel.get_all_user()
        result=[]
        for user in users:
            result.append(user.dict())
        return res(data=result, message="Users retrieved successfully")
    
    @jwt_required()
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, required=True, help='id is required',location='json')
        data = parser.parse_args()

        user_id = data['id']
        if(user_id is None):
            return res(message="id is required", code="-1",status=400)
        
        user_tuple = UserModel.find_by_id(user_id)
        if(user_tuple is None):
            return res(message="User not found", code="-1",status=404)
        (user,)=user_tuple
<<<<<<< HEAD
        permission=PermissionModel.find_by_user_id(user_id)
        if permission:
            for p in permission:
                p.delete_permission()
=======
>>>>>>> 89f9055002e6d3439cf64c3e926889812a772e4f
        user.delete_user()

        return res(message="User deleted successfully")

    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, location='json')
        parser.add_argument('password', type=str, required=True, dest='pwd', location='json')
        parser.add_argument('email', type=str, required=True, location='json')
        parser.add_argument('role', type=str, required=True, location='json')


        data = parser.parse_args()

        # valid email formate
        if not UserModel.valid_email(data['email']):
            return res(data=None, message="Invalid email format", code="-1", status=400)
        
        # valid password length > 6
        if len(data['pwd']) < 6:
            return res(data=None, message="Password length must be greater than 6", code="-1", status=400)


        if UserModel.find_by_username(data['username']):
            return res(data=None, message="User {} already exists".format(data['username']), code="-1", status=400)
        else:
            try:
                data['salt']=uuid.uuid4().hex
                data['pwd'] = generate_password_hash('{}{}'.format(data['salt'], data['pwd']))
                user = UserModel(**data)
                user.add_user()
                return res(data=None, message="User {} created successfully".format(data['username']))
            except Exception as e:
                return res(data=None, message="An error occurred while creating the user", code="-1", status=500)       


    @jwt_required()
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, required=True, help='id is required',location='json')
        parser.add_argument('username', type=str, required=False, location='json')
        parser.add_argument('password', type=str, required=False, dest='pwd', location='json')
        parser.add_argument('email', type=str, required=False, location='json')
        parser.add_argument('role', type=str, required=False, location='json')

        data = parser.parse_args()

        user_id = data['id']
        if(user_id is None):
            return res(message="id is required", code="-1",status=400)
        
        user_tuple = UserModel.find_by_id(user_id)
        if(user_tuple is None):
            return res(message="User not found", code="-1",status=404)
        (user,)=user_tuple

        if(data['username'] is not None):
            user.username = data['username']
        if(data['pwd'] is not None):
            user.salt=uuid.uuid4().hex
            user.pwd = generate_password_hash('{}{}'.format(user.salt, data['pwd']))
        if(data['email'] is not None):
            user.email = data['email']
        if(data['role'] is not None):
            user.role = data['role']

        user.update_user()

        return res(message="User edited successfully")