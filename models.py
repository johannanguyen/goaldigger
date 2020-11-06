"""Creates the database used for chat"""
import flask_sqlalchemy
from app import db


class FakeTable(db.Model):
    """Creates the Database"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    login = db.Column(db.String(200))
    image = db.Column(db.String(200))
    goal = db.Column(db.String(200))
    status = db.Column(db.String(50))
    category = db.Column(db.String(50))
    message = db.Column(db.String(50))

    def __init__(self, name, login, image, goal, status, category, message):
        self.name = name
        self.login = login
        self.image = image
        self.goal = goal
        self.status = status
        self.category = category
        self.login = message


    def __repr__(self):
        return "<Message %s>" % self.message
