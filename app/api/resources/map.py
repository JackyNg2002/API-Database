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
            ret['path_png']=os.path.join(os.getenv("HOST_URL","http://localhost:5000"),data_path,'map',map.name.split('.')[0]+".png")
            ret['path_posegraph']=os.path.join(os.getenv("HOST_URL","http://localhost:5000"),data_path,'map',map.name.split('.')[0]+".posegraph")
            ret['path_posegraphData']=os.path.join(os.getenv("HOST_URL","http://localhost:5000"),data_path,'map',map.name.split('.')[0]+".posegraphData")
            result.append(ret)
        return res(data=result, message="Success")
    
    @jwt_required()
    def post(self):
        reqparser = reqparse.RequestParser()
        reqparser.add_argument('robot_id', type=int, required=True, help='robot_id is required', location='form')
        reqparser.add_argument('name',  type=str, required=True, help='name is required',location='form')
        
        # get upload files
        reqparser.add_argument('png', type=werkzeug.datastructures.FileStorage, required=True, help='map png is required', location='files')
        reqparser.add_argument('posegraph', type=werkzeug.datastructures.FileStorage, required=True, help='posegraph is required', location='files')
        reqparser.add_argument('posegraphData', type=werkzeug.datastructures.FileStorage, required=True, help='mapData is required', location='files')
        
        args = reqparser.parse_args()

        storage_path = os.getenv("DATA_STORAGE_PATH")
        map_path = os.path.join(storage_path, 'map')
        map_png = args['png']
        map_posegraph = args['posegraph']
        map_posegraphData = args['posegraphData']
        
        

        robot_id = args['robot_id']
        name = args['name']
        if name=='':
            return res(message="Map name is required", status=400,code='-1')

        map = MapModel.find_by_name(name)
        if map:
            return res(message="Map name already exists", status=400,code='-1')
        
        if not os.path.exists(map_path):
            os.makedirs(map_path)
        map_png.save(os.path.join(map_path, args['name']+'.png'))
        map_posegraph.save(os.path.join(map_path, args['name']+'.posegraph'))
        map_posegraphData.save(os.path.join(map_path, args['name']+'.data'))

        map = MapModel(robot_id=robot_id, name=name)
        map.add_map()
        return res(message="Success")
    
    @jwt_required()
    def delete(self):
        reqparser = reqparse.RequestParser()
        reqparser.add_argument('id', type=int, required=True, help='id is required', location='json')
        args = reqparser.parse_args()
        id = args['id']
        map_tuple=MapModel.find_by_id(id)
       
        if not map_tuple:
            return res(message="Map not found", status=400,code='-1')
        
        (map,) = map_tuple
        os.remove(os.path.join(os.getenv("DATA_STORAGE_PATH"), 'map', map.name+'.png'))
        os.remove(os.path.join(os.getenv("DATA_STORAGE_PATH"), 'map', map.name+'.posegraph'))
        os.remove(os.path.join(os.getenv("DATA_STORAGE_PATH"), 'map', map.name+'.data'))
        map.delete_map()
        return res(message="Success")
    
    @jwt_required()
    def put(self):
        reqparser = reqparse.RequestParser()
        reqparser.add_argument('name', type=str, required=True, help='name is required', location='json')
        reqparser.add_argument('id', type=int, required=True, help='id is required', location='json')
        args = reqparser.parse_args()
        name = args['name']
        map = MapModel.find_by_id(args['id'])
        if not map:
            return res(message="Map not found", status=400,code='-1')
        
        (map,)=map
        #update file name
        map_path = os.path.join(os.getenv("DATA_STORAGE_PATH"), 'map')
        os.rename(os.path.join(map_path, map.name+'.png'), os.path.join(map_path, name+'.png'))
        os.rename(os.path.join(map_path, map.name+'.posegraph'), os.path.join(map_path, name+'.posegraph'))
        os.rename(os.path.join(map_path, map.name+'.data'), os.path.join(map_path, name+'.data'))

        map.name = name
        map.update_map()



        return res(message="Success")