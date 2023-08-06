from .. import database as db, flask_bcrypt, config
import pickle
import uuid
import datetime
import jwt
from itsdangerous import want_bytes

import os
key = os.getenv("SECRET_KEY")

class Session(db.Model):
    __tablename__ = "session"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    session_id = db.Column(db.String(255), unique=True)
    data = db.Column(db.LargeBinary)
    expiry = db.Column(db.DateTime)

    data_ = {}

    def get(self, key):
        return self.data_.get(key,False)

    def set(self, key, val):
        self.data_[key] = val

    def __repr__(self):
        return '<Session data %s>' % self.session_id

    @staticmethod
    def open(auth_token=None):
        if not auth_token:
            sid = str(uuid.uuid4())
            new_session = Session(session_id=sid, expiry=datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=5))
            val = pickle.dumps(dict())
            new_session.data = val
            auth_token = Session.encode_auth_token(sid=sid)
            new_session.data_["auth_token"] = auth_token
            db.session.add(new_session)
            db.session.commit()
            return new_session
        else:
            sid = Session.decode_auth_token(auth_token)
            if sid:
                saved_session = Session.query.filter_by(session_id=sid).first()
                if saved_session and saved_session.expiry <= datetime.datetime.utcnow():
                    db.session.delete(saved_session)
                    db.session.commit()
                    saved_session = None

                if saved_session:
                    val = saved_session.data
                    saved_session.data_ = pickle.loads(want_bytes(val))
                    return saved_session
            return None

    
    def delete(self):
        db.session.delete(self)
        db.session.commit()


    def save(self):
        val = pickle.dumps(dict(self.data_))
        self.data = val
        db.session.add(self)
        db.session.commit()

    @staticmethod 
    def encode_auth_token(sid):
        try:
            payload = {'sid': sid}
            return jwt.encode(
                payload,
                key,
                algorithm='HS256'
            )
        except Exception as e:
            return e
        
    @staticmethod  
    def decode_auth_token(auth_token):
        try:
            payload = jwt.decode(auth_token, key, algorithms='HS256')
            return payload["sid"]
        except:
            return False
