from ..models import db
from datetime import datetime

class RobotModel(db.Model):
    __tablename__ = 'robots'

    id = db.Column(db.Integer, primary_key=True,nullable=False,autoincrement=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    type = db.Column(db.String(255), nullable=False)
    detail = db.Column(db.String(255), nullable=True)

    permission = db.relationship('PermissionModel', backref=db.backref('robots', lazy='dynamic'))
    map = db.relationship('MapModel', backref=db.backref('maps', lazy='dynamic'))
    record = db.relationship('RecordModel', backref=db.backref('records', lazy='dynamic'))

    def add_robot(self):
        db.session.add(self)
        db.session.commit()

    def dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'detail': self.detail
        }
    
    @classmethod
    def find_by_name(cls, name):
        return db.session.execute(db.select(cls).filter_by(name = name)).first()
    
    @classmethod
    def get_all_robot(cls):
        return db.session.query(cls).all()
    
    
