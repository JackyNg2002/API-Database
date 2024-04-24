from ..models import db
from datetime import datetime

class UserModel(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True,nullable=False,autoincrement=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    # role only has two values: 'admin' and 'user' add constraint to limit the value
    role = db.Column(db.Enum('admin','manager', 'user','robot'), default='user', comment='role',nullable=False)

    pwd = db.Column(db.String(102), comment='password')
    salt = db.Column(db.String(32), comment='salt')

    def add_user(self):
        db.session.add(self)
        db.session.commit()
    def delete_user(self):
        db.session.delete(self)
        db.session.commit()
    
    def update_user(self):
        db.session.commit()

    def dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'roles': [self.role],
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
    def find_by_id(cls, id):
        return db.session.execute(db.select(cls).filter_by(id = id)).first()
    
    @classmethod
    def get_all_user(cls):
        return db.session.query(cls).all()
    
    @classmethod
    def valid_email(cls, email):
        return '@' in email