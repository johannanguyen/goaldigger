""" models.py to store all tables in DB """
from datetime import datetime
from app import db


class Users(db.Model):
    """Table for users"""

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200))
    name = db.Column(db.String(50), nullable=False)
    img_url = db.Column(db.String())
    signed_in = db.Column(db.String(5))
    google_id = db.Column(db.String(3000))
    # fb_id = db.Column(db.String())
    # bio = db.Column(db.String())

    def __init__(self, email, name, img_url, signed_in, google_id):
        """vars for users"""
        self.name = name
        self.email = email
        self.img_url = img_url
        self.signed_in = signed_in
        self.google_id = google_id


class Goals(db.Model):
    """Table for goals"""

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    description = db.Column(db.String())
    progress = db.Column(db.String())
    date = db.Column(db.DateTime, default=datetime.now)
    post_text = db.Column(db.String())

    def __init__(self, user_id, category, description, progress, post_text):
        """vars for goals"""
        self.user_id = user_id
        self.category = category
        self.description = description
        self.progress = progress
        self.post_text = post_text
