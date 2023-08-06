from .blacklist import BlacklistToken
from .session import Session
from ..api import database as db, flask_bcrypt, config

from flask import request
class Auth(db.Model):
    __tablename__ = "auth"

    aid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=True )

    user_type = db.Column(db.String(255), nullable=True)

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = flask_bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return flask_bcrypt.check_password_hash(self.password_hash, password)

    @staticmethod
    def login(email, password, user_type=None):
        try:
            auth = Auth.query.filter_by(email=email).first()
            if auth and auth.check_password(password):
                if not user_type or (user_type and auth.user_type == user_type):
                    session = Session.open()
                    session.save()
                    return session
                return False
            else:
                return False
        except Exception as e:
            return None
    
    @staticmethod
    def get_session():
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                auth_token = auth_header.split(" ")[1]
            except IndexError:
                return None
        else:
            auth_token = None

        if auth_token:
            session = Session.open(auth_token)
            
            if session:
                return session
            return None
        else:
            return None

