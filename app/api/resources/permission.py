

from flask_restful import Resource,reqparse
from flask_jwt_extended import jwt_required
from ..models.permission import PermissionModel
from ..models.user import UserModel
from ..common.utils import res

class PermissionService(Resource):
    @jwt_required()
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('robot_id', type=int, required=False, help='robot_id is required',location='args')
        parser.add_argument('user_id', type=int, required=False, help='map_id is required' ,location='args')
        
        data = parser.parse_args()
        robot_id = data['robot_id']
        user_id = data['user_id']

        permissions = PermissionModel.get_all_permission(robot_id,user_id)
        result=[]
        for permission in permissions:
            result.append(permission.dict())
        return res(data=result, message="Permissions retrieved successfully")
    
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('robot_ids', type=list[int], required=True, help='robot_ids is required',location='json')
        parser.add_argument('user_name', type=str, required=True, help='user_name is required',location='json')
        
        data = parser.parse_args()
        robot_ids = data['robot_ids']
        user_name = data['user_name']

        if(user_name is None):
            return res(message="user_name is required", code="-1",status=400)

        user_tuple = UserModel.find_by_username(user_name)
        if(user_tuple is None):
            return res(message="User not found", code="-1",status=404)
        (user,)=user_tuple
        user_id = user.id

        if(robot_ids is None or user_id is None):
            return res(message="robot_ids and user_name is required", code="-1",status=400)
        
        permissions_tuple:tuple[PermissionModel]= PermissionModel.find_by_user_id(user_id)

        permissions_dict:dict[int,PermissionModel]={}
        for (permission,) in permissions_tuple:
            permissions_dict[permission.robot_id]=permission
            
        # print("----------------------------------------------")
        # print(permissions_dict)
        # print("----------------------------------------------")

        for robot_id in robot_ids:
            if(robot_id in permissions_dict):
                del permissions_dict[robot_id]
                continue
            permission = PermissionModel(user_id=user_id,robot_id=robot_id)
            permission.add_permission()


        for robot_id in permissions_dict:
            permission = permissions_dict[robot_id]
            permission.delete_permission()
        
        return res(message="Permissions edited successfully")
        
        
