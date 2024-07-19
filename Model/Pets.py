import base64

from PBD_config import db_init as db


class Pets(db.Model):
    __tablename__ = 'pets'
    Pno = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    Pname = db.Column(db.String(255), nullable=False)
    Powner = db.Column(db.String(255), db.ForeignKey('users.Uid'), nullable=False)
    Pimage = db.Column(db.LargeBinary, nullable=True)
    Pgender = db.Column(db.String(255), nullable=False)
    Pvariety = db.Column(db.String(255), nullable=False)
    Pbirth = db.Column(db.Date)

    def to_dict(self):
        return {
            'Pno': self.Pno,
            'Pname': self.Pname,
            'Powner': self.Powner,
            'Pimage': base64.b64encode(self.Pimage).decode('utf-8'),
            'Pgender': self.Pgender,
            'Pvariety': self.Pvariety,
            'Pbirth': self.Pbirth.strftime('%Y-%m-%d') if self.Pbirth else None
        }
