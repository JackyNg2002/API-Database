import os
import werkzeug

from flask_restful import Resource ,reqparse
from flask_jwt_extended import jwt_required
from ..models.record import RecordModel
from ..common.utils import res

class RecordService(Resource):
    @jwt_required()
    def get(self):
        allrecord = RecordModel.get_all_record()
        data_path = os.getenv("DATA_STORAGE_PATH")
        result = []
        for record in allrecord:
            ret=record.dict()
            ret['path']=os.path.join(os.getenv("HOST_URL","http://localhost:5000"),data_path,'record',record.robot_id,record.name)
            result.append(record.dict())
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
        record_file = args['record']
        robot_id = args['robot_id']
        name = args['name']
        record = RecordModel.find_by_name(name)
        if record:
            return res(message="Record name already exists", status=400, code='-1')
        if not os.path.exists(record_path):
            os.makedirs(record_path)
        record_file.save(os.path.join(record_path, str(robot_id), name))
        record = RecordModel(robot_id=robot_id, name=name)
        record.add_record()
        return res(message="Success")
    
    @jwt_required()
    def delete(self):
        reqparser = reqparse.RequestParser()
        reqparser.add_argument('name', type=str, required=True, help='name is required', location='json')
        args = reqparser.parse_args()
        name = args['name']
        record = RecordModel.find_by_name(name)
        if not record:
            return res(message="Record not found", status=400, code='-1')
        
        #delete record file
        (record,) = record
        storage_path = os.getenv("DATA_STORAGE_PATH")
        record_path = os.path.join(storage_path, 'record')
        os.remove(os.path.join(record_path, str(record.robot_id), name))

        record.delete_record()
        return res(message="Success")
    
    @jwt_required()
    def put(self):
        reqparser = reqparse.RequestParser()
        reqparser.add_argument('name', type=str, required=True, help='name is required', location='json')
        reqparser.add_argument('new_name', type=str, required=True, help='new_name is required', location='json')
        args = reqparser.parse_args()
        name = args['name']
        new_name = args['new_name']
        record = RecordModel.find_by_name(name)
        if not record:
            return res(message="Record not found", status=400, code='-1')
        (record,) = record
        record.name = new_name
        record.update_record()

        #rename record file
        storage_path = os.getenv("DATA_STORAGE_PATH")
        record_path = os.path.join(storage_path, 'record')
        os.rename(os.path.join(record_path, str(record.robot_id), name),os.path.join(record_path, str(record.robot_id), new_name))
        
        return res(message="Success")