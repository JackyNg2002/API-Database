from ..models import db
from datetime import datetime

class MapModel(db.Model):
    
    __tablename__ = 'maps'

    id = db.Column(db.Integer, primary_key=True,nullable=False,autoincrement=True)
    robot_id = db.Column(db.Integer, db.ForeignKey('robots.id'), nullable=False)
    robot=db.relationship('RobotModel',backref=db.backref('maps',lazy='dynamic'))
    datetime = db.Column(db.DateTime, default=datetime.now, nullable=False)
    name = db.Column(db.String(255), nullable=False, unique=True)

    def add_map(self):
        db.session.add(self)
        db.session.commit()
    
    def dict(self):
        return {
            'id': self.id,
            'robot_id': self.robot_id,
            'datetime': self.datetime,
            'name': self.name
        }
    
    @classmethod
    def find_by_name(cls, name):
        return db.session.execute(db.select(cls).filter_by(name = name)).first()
    
    @classmethod
    def get_all_map(cls):
        return db.session.query(cls).all()
