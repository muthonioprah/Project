from sqlalchemy.orm import backref
from main import db
from werkzeug.security import check_password_hash

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    phone_number = db.Column(db.String(80), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=False)
    password = db.Column(db.String(255), nullable=False)

    biasharas = db.relationship("Biashara", backref="user", cascade="all, delete, delete-orphan")
    disposables = db.relationship("Disposable", backref="user", cascade="all, delete, delete-orphan")

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def all(cls):
        return cls.query.all()

    @classmethod
    def get_user_by_email(cls,email:str):
        return cls.query.filter_by(email=email).first()

    # check email exists
    @classmethod
    def check_email_exists(cls, email: str) -> bool:
        record = user = cls.query.filter_by(email=email).first()
        if record:
            return True
        else: 
            return False


    # validate password
    @classmethod
    def validate_password(cls, email:str, password:str):
        # get user
        user = cls.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            return True
        else:
            return False