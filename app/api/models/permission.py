from ..models import db
from datetime import datetime

class PermissionModel(db.Model):
    
    __tablename__ = 'permissions'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True, nullable=False)
    user = db.relationship('UserModel', backref=db.backref('permissions', lazy='select'))
    robot_id = db.Column(db.Integer, db.ForeignKey('robots.id'), primary_key=True, nullable=False)
    robot = db.relationship('RobotModel', backref=db.backref('permissions', lazy='select'))

    def add_permission(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_permission(self):
        db.session.delete(self)
        db.session.commit()

    def dict(self):
        return {
            'user_id': self.user_id,
            'robot_id': self.robot_id
        }
    
    @classmethod
    def find_by_user_id(cls, user_id):
        return db.session.execute(db.select(cls).filter_by(user_id = user_id)).all()
    
    @classmethod
    def find_by_robot_id(cls, robot_id):
        return db.session.execute(db.select(cls).filter_by(robot_id = robot_id)).all()
    
    @classmethod
    def find_by_robot_id_model(cls,robot_id)->list:
        return db.session.query(cls).filter_by(robot_id=robot_id).all()
    
    @classmethod
    def find_by_user_id_model(cls,user_id)->list:
        return db.session.query(cls).filter_by(user_id=user_id).all()
    
    @classmethod
    def get_all_permission(cls):
        return db.session.query(cls).all()
    
    @classmethod
    def get_all_permission(cls,robot_id,user_id):
        if(robot_id is None and user_id is None):
            return db.session.query(cls).all()
        elif(robot_id is None):
            return db.session.query(cls).filter_by(user_id=user_id).all()
        elif(user_id is None):
            return db.session.query(cls).filter_by(robot_id=robot_id).all()
        return db.session.query(cls).filter_by(robot_id=robot_id,user_id=user_id).all()
    
    @classmethod
    def is_exist(cls,robot_id,user_id):
        return db.session.query(cls).filter_by(robot_id=robot_id,user_id=user_id).first() is not None


