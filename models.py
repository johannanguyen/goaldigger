from datetime import datetime
import flask_sqlalchemy
from app import db
from enum import Enum

#When someone logs in, check which auth method they used. If they used google, then check google_id to see if they had created an account. 
#If there aren't any users with that google_id, create one. Same for facebook auth.
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(35), nullable=False)
    google_id = db.Column(db.String())
    fb_id = db.Column(db.String())
    img_url = db.Column(db.String())
    #bio = db.Column(db.String())
    
    def __init__(self, name, email, img_url=None, google_id=None, fb_id=None):
        self.name = name
        self.email = email
        #self.bio = bio
        if google_id:
            self.google_id = google_id
        if fb_id:
            self.fb_id = fb_id
        if img_url:
            self.img_url = img_url
            
            
class Goals(db.Model):
    '''Table for goals'''
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    description = db.Column(db.String())
    progress = db.Column(db.String())
    date = db.Column(db.DateTime, default=datetime.now)
    text = db.Column(db.String())
    
    def __init__(self, user_id, category, description, progress):
        self.user_id = user_id
        self.category = category
        self.description = description
        self.progress = progress
        self.text = text
        
        

# class Posts(db.Model):
#     '''Table for user posts'''
#     id = db.Column(db.Integer, primary_key=True)
#     category = db.Column(db.String())
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
#     title = db.Column(db.String())
#     text = db.Column(db.String())
#     date = db.Column(db.DateTime, default=datetime.now)
    
#     def __init__(self, user_id, category, title, text):
#         self.user_id = user_id
#         self.category = category
#         self.title = title
#         self.text = text

# class Messages(db.Model):
#     '''Table for chat messages.'''
#     id = db.Column(db.Integer, primary_key=True)
#     text = db.Column(db.String(300))
#     date = db.Column(db.DateTime, default=datetime.now)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

#     def __init__(self, text, user_id):
#         self.text = text
#         self.user_id = user_id

#     def __repr__(self):
#         return "<Text: {}\nBy: {}>\n".format(self.text, self.user)
        
        
# class Groups(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     category = db.Column(db.String())
#     description = db.Column(db.String())
#     name = db.Column(db.String())
#     sidebar_text = db.Column(db.String())
#     created = db.Column(db.DateTime, default=datetime.now)
    
#     def __init__(self, category, description, name, sidebar_text):
#         self.category = category
#         self.description = description
#         self.name = name
#         self.sidebar_text = sidebar_text
        
# class Groups_Users(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
#     group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))
    
#     def __init__(self, user_id, group_id):
#         self.user_id = user_id
#         self.group_id = group_id


# Maybe this Enum is unnecesary.
# class Progress(Enum):
#     IN_PROGRESS = "in progress"
#     FINISHED = "completed"

# class Categories(Enum):
#     WORK = "work"
#     EXERCISE = "exercise"
#     ...
