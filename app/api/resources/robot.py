
from flask_restful import Resource,reqparse
from flask_jwt_extended import jwt_required
from ..models.robot import RobotModel
from ..common.utils import res

class RobotService(Resource):
    @jwt_required()
    def get(self):
        reqparser = reqparse.RequestParser()
        reqparser.add_argument('name',type=str,required=False,help='name is required',location='args')
        args = reqparser.parse_args()
        if args['name']:
            robot = RobotModel.find_by_name(args['name'])
            if not robot:
                return res(message="Robot not found", status=400, code='-1')
            (robot,) = robot
            return res(data=robot.dict(), message="Robot retrieved successfully")

        robots = RobotModel.get_all_robot()
        result=[]
        for robot in robots:
            result.append(robot.dict())
        return res(data=result, message="Robots retrieved successfully")
    
    @jwt_required()
    def post(self):
        reqparser = reqparse.RequestParser()
        reqparser.add_argument('name', type=str, required=True, help='name is required', location='json')
        reqparser.add_argument('type', type=str, required=True, help='type is required', location='json')
        reqparser.add_argument('detail', type=str, required=False, help='detail is required', location='json')

        args = reqparser.parse_args()

        robot = RobotModel.find_by_name(args['name'])
        if robot:
            return res(message="Robot name already exists", status=400, code='-1')
        if args['detail'] is None:
            args['detail'] = ""
        robot = RobotModel(name=args['name'], type=args['type'], detail=args['detail'])
        robot.add_robot()
        return res(message="Robot added successfully")
    
    @jwt_required()
    def put(self):
        reqparser = reqparse.RequestParser()
        reqparser.add_argument('id', type=int, required=True, help='id is required', location='json')
        reqparser.add_argument('name', type=str, required=True, help='name is required', location='json')
        reqparser.add_argument('type', type=str, required=True, help='type is required', location='json')
        reqparser.add_argument('detail', type=str, required=False, help='detail is required', location='json')

        args = reqparser.parse_args()
        robot = RobotModel.find_by_id(args['id'])
        if not robot:
            return res(message="Robot not found", status=400, code='-1')
        if args['detail'] is None:
            args['detail'] = ""
        (robot,) = robot
        robot.name = args['name']
        robot.type = args['type']
        robot.detail = args['detail']
        robot.update_robot()
        return res(message="Robot updated successfully")
    
    @jwt_required()
    def delete(self):
        reqparser = reqparse.RequestParser()
        reqparser.add_argument('id', type=int, required=True, help='id is required', location='json')
        args = reqparser.parse_args()
        robot = RobotModel.find_by_id(args['id'])
        if not robot:
            return res(message="Robot not found", status=400, code='-1')
        (robot,) = robot
        robot.delete_robot()
        return res(message="Robot deleted successfully")
    