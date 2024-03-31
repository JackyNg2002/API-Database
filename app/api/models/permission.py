from ..models import db
from datetime import datetime

class PermissionModel(db.Model):
    
    __tablename__ = 'permissions'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True, nullable=False)
    user = db.relationship('UserModel', backref=db.backref('permissions', lazy='dynamic'))
    robot_id = db.Column(db.Integer, db.ForeignKey('robots.id'), primary_key=True, nullable=False)
    robot = db.relationship('RobotModel', backref=db.backref('permissions', lazy='dynamic'))

    def add_permission(self):
        db.session.add(self)
        db.session.commit()

    def dict(self):
        return {
            'user_id': self.user_id,
            'robot_id': self.robot_id
        }
    
    @classmethod
    def find_by_user_id(cls, user_id):
        return db.session.execute(db.select(cls).filter_by(user_id = user_id)).first()
    
    @classmethod
    def find_by_robot_id(cls, robot_id):
        return db.session.execute(db.select(cls).filter_by(robot_id = robot_id)).first()
    
    @classmethod
    def get_all_permission(cls):
        return db.session.query(cls).all()

