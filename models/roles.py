from sqlalchemy.orm import backref
from main import db
from sqlalchemy import func

class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    role = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_ = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    users = db.relationship("User", backref="role", cascade="all, delete, delete-orphan")

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def all(cls):
        return cls.query.all()

    @classmethod
    def check_role_exists(cls, name:str) ->bool:
        record = cls.query.filter_by(role=name).first()
        if record:
            return True
        else:
            return False