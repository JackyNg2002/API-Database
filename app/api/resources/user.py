from flask_restful import Resource
from flask_jwt_extended import jwt_required
from ..models.user import UserModel
from ..common.utils import res

class UserService(Resource):
    def get(self):
        users = UserModel.get_all_user()
        result=[]
        print("----------------------------------------------")
        print(users)
        for user in users:
            result.append(user.dict())

        print(result)
        return res(data=result, message="Users retrieved successfully", code=0, status=200)