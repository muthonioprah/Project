from main import db
from sqlalchemy import func

class DisposableBooking(db.Model):
    __tablename__ = "disposable_bookings"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(255), nullable=False)
    disposable_id = db.Column(db.Integer, db.ForeignKey("disposable.id"))
    created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_ = db.Column(db.DateTime(timezone=True), onupdate=func.now())  


    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def all(cls):
        return cls.query.all()

    @classmethod
    def check_email_exists(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def fetch_by_disposable_id(cls, id):
        r = cls.query.filter_by(disposable_id=id).all()
        return r