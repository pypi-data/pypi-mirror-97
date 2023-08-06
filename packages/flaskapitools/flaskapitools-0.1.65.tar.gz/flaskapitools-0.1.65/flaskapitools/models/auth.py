from .blacklist import BlacklistToken
from ..api import database as db, flask_bcrypt, config


class Auth(db.Model):
    __tablename__ = "auth"

    aid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    passsword_hash = db.Column(db.String(255), nullable=True )

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
            user = Auth.query.filter_by(email=data.get('email')).first()
            if user and user.check_password(data.get('password')):
                return True
            else:
                return False
        except Exception as e:
            return None
