import base64

from sqlalchemy import func

from PBD_config import db_init as db
from datetime import datetime


class Behavior(db.Model):
    __tablename__ = 'behavior'
    Bno = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    Bowner_id = db.Column(db.String(255), db.ForeignKey('users.Uid'), nullable=False)
    Btime = db.Column(db.DateTime, default=func.now(), nullable=False)
    Bclass = db.Column(db.String(255), nullable=False)
    Bconfidence = db.Column(db.String(255), nullable=False)
    Bphoto = db.Column(db.LargeBinary, nullable=False)

    def to_dict(self):
        return {
            'Bno': self.Bno,
            'Bowner_id': self.Bowner_id,
            'Btime': self.Btime.strftime('%Y-%m-%d %H:%M:%S'),
            'Bclass': self.Bclass,
            'Bconfidence': self.Bconfidence,
            'Bphoto': base64.b64encode(self.Bphoto).decode('utf-8')
        }
