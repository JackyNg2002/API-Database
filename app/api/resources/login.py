from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token,jwt_required,get_jwt_identity
from werkzeug.security import check_password_hash

from ..schema.register_sha import reg_args_valid
from ..models.user import UserModel
from ..common.utils import res


class Login(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        reg_args_valid(parser)
        data = parser.parse_args()

        username = data['username']
        user_tuple  = UserModel.find_by_username(username)

        if user_tuple:
            try:
                (user,)=user_tuple
                pwd,salt=user.getPwd().get('pwd'),user.getPwd().get('salt')
                valid=check_password_hash(pwd, '{}{}'.format(salt, data['pwd']))
                if valid:
                    response_data=generateToken(username)
                    return res(data=response_data, message="Login successful", code=0, status=200)
                else:
                    raise Exception('Invalid password')
            except Exception as e:
                return res( message='Error: {}'.format(e), code=-1,status=500)
        else:
            return res( message='User {} does not exist'.format(username), code=-1,status=400)
        
    @jwt_required(refresh=True)
    def get(self):
        current_username=get_jwt_identity()

        access_token=create_access_token(identity=current_username)
        return res(data={'access_token':'Bearer '+access_token}, message='Token refreshed', code=0, status=200)

def generateToken(id):
    access_token = create_access_token(identity=id)
    refresh_token = create_refresh_token(identity=id)
    return {
        'access_token':'Bearer '+ access_token,
        'refresh_token':'Bearer '+ refresh_token}