from ..models import db
from datetime import datetime

class RobotModel(db.Model):
    __tablename__ = 'robots'

    id = db.Column(db.Integer, primary_key=True,nullable=False,autoincrement=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    type = db.Column(db.String(255), nullable=False)
    detail = db.Column(db.String(255), nullable=True)

    permission = db.relationship('PermissionModel', backref=db.backref('robots', lazy='select'))
    map = db.relationship('MapModel', backref=db.backref('maps', lazy='select'))
    record = db.relationship('RecordModel', backref=db.backref('records', lazy='select'))

    def add_robot(self):
        db.session.add(self)
        db.session.commit()

    def update_robot(self):
        db.session.commit()
    
    def delete_robot(self):
        db.session.delete(self)
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
    def find_by_id(cls, id):
        return db.session.execute(db.select(cls).filter_by(id = id)).first()
    
    @classmethod
    def get_all_robot(cls):
        return db.session.query(cls).all()
    
    
