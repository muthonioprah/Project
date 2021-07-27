from sqlalchemy.orm import backref
from main import db
from sqlalchemy import func

class Biashara(db.Model):
    __tablename__ = "biashara"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    thumbnail = db.Column(db.String(255), nullable=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    contact_email = db.Column(db.String(255), nullable=False)
    contact_number = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_ = db.Column(db.DateTime(timezone=True), onupdate=func.now())  

    disposables = db.relationship("Disposable", backref="biashara", cascade="all, delete, delete-orphan")

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def all(cls):
        return cls.query.all()

    @classmethod
    def user_biashara(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()

    @classmethod
    def get_biashara_by_id(cls, id:int):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def check_biashara_exists(cls, name: str):
        record = cls.query.filter_by(name=name).first()
        if record:
            return True
        else:
            return False

    @classmethod
    def update(cls,id, business_name, description, email, phone):
        record = cls.query.filter_by(id=id).first()
        if record:
            record.name = business_name
            record.description = description
            record.email = email
            record.contact_number = phone

            db.session.commit()

            return True