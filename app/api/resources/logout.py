from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt

from ..models.revoked_token import RevokedTokenModel
from ..common.utils import res

class Logout(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()['jti']
        
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            return res(message="Successfully logged out", code=0, status=200)
        except Exception as e:
            return res(message="Error: {}".format(e), code=-1, status=500)