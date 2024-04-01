import os
import werkzeug

from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from ..models.map import MapModel
from ..common.utils import res, format_datetime_to_json

class MapService(Resource):
    @jwt_required()
    def get(self):
        
        allmap = MapModel.get_all_map()
        data_path = os.getenv("DATA_STORAGE_PATH")
        result = []
        for map in allmap:
            ret = map.dict()
            ret['datetime'] = format_datetime_to_json(ret["datetime"],"%Y-%m-%d %H:%M:%S")
            ret['path']=os.path.join(os.getenv("HOST_URL","http://localhost:5000"),data_path,'map',map.name.split('.')[0]+".png")
            result.append(ret)
        return res(data=result, message="Success")
    
    @jwt_required()
    def post(self):
        reqparser = reqparse.RequestParser()
        reqparser.add_argument('robot_id', type=int, required=True, help='robot_id is required', location='form')
        reqparser.add_argument('name',  type=str, required=True, help='name is required',location='form')
        
        # get upload files
        reqparser.add_argument('png', type=werkzeug.datastructures.FileStorage, required=True, help='map png is required', location='files')
        
        args = reqparser.parse_args()

        storage_path = os.getenv("DATA_STORAGE_PATH")
        map_path = os.path.join(storage_path, 'map')
        map_png = args['png']
        
        

        robot_id = args['robot_id']
        name = args['name']
        map = MapModel.find_by_name(name)
        if map:
            return res(message="Map name already exists", status=400,code='-1')
        
        if not os.path.exists(map_path):
            os.makedirs(map_path)
        map_png.save(os.path.join(map_path, args['name']+'.png'))
        map = MapModel(robot_id=robot_id, name=name)
        map.add_map()
        return res(message="Success")
    
    @jwt_required()
    def delete(self):
        reqparser = reqparse.RequestParser()
        reqparser.add_argument('name', type=str, required=True, help='name is required', location='json')
        args = reqparser.parse_args()
        name = args['name']
        map_tuple=MapModel.find_by_name(name)
       
        if not map_tuple:
            return res(message="Map not found", status=400,code='-1')
        
        (map,) = map_tuple
        os.remove(os.path.join(os.getenv("DATA_STORAGE_PATH"), 'map', name+'.png'))
        map.delete_map()
        return res(message="Success")
    
    @jwt_required()
    def put(self):
        reqparser = reqparse.RequestParser()
        reqparser.add_argument('name', type=str, required=True, help='name is required', location='json')
        reqparser.add_argument('new_name', type=str, required=True, help='new_name is required', location='json')
        args = reqparser.parse_args()
        name = args['name']
        new_name = args['new_name']
        map = MapModel.find_by_name(name)
        if not map:
            return res(message="Map not found", status=400,code='-1')
        
        (map,)=map
        map.name = new_name
        map.update_map()

        #update file name
        map_path = os.path.join(os.getenv("DATA_STORAGE_PATH"), 'map')
        os.rename(os.path.join(map_path, name+'.png'), os.path.join(map_path, new_name+'.png'))

        return res(message="Success")