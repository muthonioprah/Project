from main import db
from sqlalchemy import func

class Disposable(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(250), nullable=False)
    brief_description = db.Column(db.String(255), nullable=False)
    details = db.Column(db.Text, nullable=False)
    biashara_id = db.Column(db.Integer, db.ForeignKey("biashara.id"))
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    is_published = db.Column(db.Boolean, default=True)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_ = db.Column(db.DateTime(timezone=True), onupdate=func.now())  

    bookings = db.relationship("DisposableBooking", cascade="all, delete, delete-orphan")


    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def all(cls):
        return cls.query.all()

    @classmethod
    def all_user_disposables(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()

    @classmethod
    def fetch_by_biashara_id(cls, id:int):
        return cls.query.filter_by(biashara_id=id).all()

    @classmethod
    def published(cls):
        r = cls.query.filter_by(is_published=True)
        return r

    @classmethod
    def user_published(cls, user_id):
        r = cls.query.filter_by(is_published=True, user_id=user_id)
        return r

    @classmethod
    def user_not_published(cls, user_id:int):
        r = cls.query.filter_by(is_published=False,user_id=user_id).all()
        return r

    @classmethod
    def update(cls, id, title, brief_description,details):
        record = cls.query.filter_by(id=id).first()
        if record:
            record.title = title
            record.brief_description = brief_description
            record.details = details

            db.session.commit()

            return True

    @classmethod
    def change_publish_status(cls,id):
        record = cls.query.filter_by(id=id).first()
        if record.is_published == True:
            record.is_published = False
            db.session.commit()
        else:
            record.is_published = True
            db.session.commit()
            
