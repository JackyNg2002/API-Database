from flask_restful import Resource
from flask_jwt_extended import jwt_required , get_jwt_identity
from ...models.user import UserModel
from ...common.utils import res

class User(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        user_tuple = UserModel.find_by_username(current_user)
        if(user_tuple is None):
            return res(data=None, message="User not found", code="-1", status=404)
        (user,)=user_tuple
        result = user.dict()
        return res(data=result, message="User retrieved successfully")
    
