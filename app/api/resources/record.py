import os
import werkzeug

from flask_restful import Resource ,reqparse
from flask_jwt_extended import jwt_required
from ..models.record import RecordModel
from ..common.utils import res,format_datetime_to_json

class RecordService(Resource):
    @jwt_required()
    def get(self):

        reqparser = reqparse.RequestParser()
<<<<<<< HEAD
        reqparser.add_argument('robot_id', type=int, required=False, help='robot_id is required', location='args',default=None)
        reqparser.add_argument('limit', type=int, required=False, help='limit is required', location='args',default=None)
        reqparser.add_argument('offset', type=int, required=False, help='offset is required', location='args',default=None)

        args = reqparser.parse_args()
        robot_id = args['robot_id']
        limit = args['limit']
        offset = args['offset']

        allrecord = RecordModel.get_all_record(robot_id=robot_id,limit=limit,offset=offset)
        total = len(allrecord)
        data_path = os.getenv("DATA_STORAGE_PATH")
        result = {'record':[],'total':total}
        for record in allrecord:
            ret=record.dict()
            # if robot_id != None and record.robot_id != robot_id:
            #     continue
            ret['path']=os.path.join(os.getenv("HOST_URL","http://localhost:5000"),data_path,'record',str(record.robot_id),record.name)
            ret['datetime']=format_datetime_to_json(ret['datetime'])
            
            result['record'].append(ret)
=======
        reqparser.add_argument('robot_id', type=int, required=False, help='robot_id is required', location='args')
        args = reqparser.parse_args()
        robot_id = args['robot_id']

        allrecord = RecordModel.get_all_record()
        data_path = os.getenv("DATA_STORAGE_PATH")
        result = []
        for record in allrecord:
            ret=record.dict()
            if robot_id != None and record.robot_id != robot_id:
                continue
            ret['path']=os.path.join(os.getenv("HOST_URL","http://localhost:5000"),data_path,'record',str(record.robot_id),record.name)
            ret['datetime']=format_datetime_to_json(ret['datetime'])
            result.append(ret)
>>>>>>> 89f9055002e6d3439cf64c3e926889812a772e4f
        return res(data=result, message="Success")
    
    @jwt_required()
    def post(self):
        reqparser = reqparse.RequestParser()
        reqparser.add_argument('robot_id', type=int, required=True, help='robot_id is required', location='form')
        reqparser.add_argument('name', type=str, required=True, help='name is required', location='form')   
        reqparser.add_argument('record', type=werkzeug.datastructures.FileStorage, required=True, help='record is required', location='files')

        args = reqparser.parse_args()
        storage_path = os.getenv("DATA_STORAGE_PATH")
        record_path = os.path.join(storage_path, 'record')
        save_path = os.path.join(record_path, str(args['robot_id']))
        record_file = args['record']
        robot_id = args['robot_id']
        name = args['name']
        record = RecordModel.find_by_name(name)
        if record:
            return res(message="Record name already exists", status=400, code='-1')
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        record_file.save(os.path.join(save_path,  name))
        record = RecordModel(robot_id=robot_id, name=name)
        record.add_record()
        return res(message="Success")
    
    @jwt_required()
    def delete(self):
        reqparser = reqparse.RequestParser()
        reqparser.add_argument('id', type=int, required=True, help='id is required', location='json')
        args = reqparser.parse_args()
        id = args['id']
        record = RecordModel.find_by_id(id)
        if not record:
            return res(message="Record not found", status=400, code='-1')
        
        #delete record file
        (record,) = record
        storage_path = os.getenv("DATA_STORAGE_PATH")
        record_path = os.path.join(storage_path, 'record')
        os.remove(os.path.join(record_path, str(record.robot_id), record.name))

        record.delete_record()
        return res(message="Success")
    
    @jwt_required()
    def put(self):
        reqparser = reqparse.RequestParser()
        reqparser.add_argument('name', type=str, required=True, help='name is required', location='json')
        reqparser.add_argument('id', type=int, required=True, help='id is required', location='json')
        args = reqparser.parse_args()
        name = args['name']
        id = args['id']
        record = RecordModel.find_by_id(id)
        if not record:
            return res(message="Record not found", status=400, code='-1')
        (record,) = record
        #rename record file
        storage_path = os.getenv("DATA_STORAGE_PATH")
        record_path = os.path.join(storage_path, 'record')
        os.rename(os.path.join(record_path, str(record.robot_id), record.name),os.path.join(record_path, str(record.robot_id), name))

        record.name = name
        record.update_record()

       
        
        return res(message="Success")