from ..models import db
from datetime import datetime

class UserModel(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True,nullable=False,autoincrement=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    pwd = db.Column(db.String(102), comment='password')
    salt = db.Column(db.String(32), comment='salt')

    def add_user(self):
        db.session.add(self)
        db.session.commit()

    def dict(self):
        return {
            'id': self.id,
            'username': self.username,
        }
    def getPwd(self):
        return {
            'pwd': self.pwd,
            'salt': self.salt
        }
    
    @classmethod
    def find_by_username(cls, username):
        return db.session.execute(db.select(cls).filter_by(username = username)).first()
    
    @classmethod
    def get_all_user(cls):
        return db.session.query(cls).all()
    