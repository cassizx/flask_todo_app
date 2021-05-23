import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from app import db


class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String())
    subject = db.Column(db.String())
    text = db.Column(db.String())
    create_date = db.Column(db.DateTime(), default=datetime.datetime.now())
    done_date = db.Column(db.DateTime())
    owner = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, state, subject, text, owner):
        self.state = state
        self.subject = subject
        self.text = text
        self.owner = owner


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    email_is_confurmed = db.Column(db.Boolean(), default=False)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    create_date = db.Column(db.DateTime(), default=datetime.datetime.now())


    def __init__(self, email, password, name):
        self.email = email
        self.password = password
        self.name = name