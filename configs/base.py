import os

class Base:
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SECRET_KEY = os.environ.get("SECRET_KEY")

class Development(Base):
    FLASK_APP = os.environ.get("FLASK_APP")
    FLASK_ENV = os.environ.get("FLASK_ENV")
    # SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI =os.environ.get("SQLALCHEMY_DATABASE_URI")
    