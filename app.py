import os
from os.path import join, dirname
import flask
from flask import Flask, render_template
import flask_socketio
import flask_sqlalchemy
from dotenv import load_dotenv
import requests
from flask import request
from datetime import datetime
#SQLALCHEMY_TRACK_MODIFICATIONS = False

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
server_socket = flask_socketio.SocketIO(app)
server_socket.init_app(app, cors_allowed_origins="*")

dotenv_path = join(dirname(__file__), "sql.env")
load_dotenv(dotenv_path)
database_uri = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_DATABASE_URI"] = database_uri

db = flask_sqlalchemy.SQLAlchemy(app)
db.init_app(app)
db.app = app

db.create_all()
db.session.commit()

import models


EMIT_EXERCISE_NEWSFEED_CHANNEL = "homepage"
GOOGLE_INFO_RECEIVED_CHANNEL = "google info received"

def emit_newsfeed(channel, sid):
    all_goals = [
        {
            "user_id": db_users.id,
            "username": db_users.name,
            "img_url": db_users.img_url,
            "category": db_goals.category,
            "description": db_goals.description,
            "progress": db_goals.progress,
            "post_text": db_goals.post_text
        }
        for db_users, db_goals in\
        db.session.query(models.Users, models.Goals)\
        .filter(models.Users.id == models.Goals.user_id)\
        .order_by(models.Goals.date).all()
    ]
    
    server_socket.emit(channel, all_goals, sid)



def push_new_user_to_db(email, username, image, is_signed_in, id_token):
    db.session.add(models.Users(email, username, image, is_signed_in, id_token));
    db.session.commit();


@server_socket.on('new google user')
def on_new_google_user(data):
    # Grabs all of the users CURRENTLY in the database
    # Grabs the new google login email and checks to see if it is in the list of emails
    #     If it is not, it will add that user to the database
    # The email array will have to be repopulated (to account for newly added user)
    # primary_id is determined by taking the index of where the email is located in the email array + 1
    #     example:
    #         all_emails = [johanna@gmail.com, joey@gmail.com]
    #         johanna's primary id = 0 + 1 = 1
    # Grabs all the goals and progress in the database relating to the primary id
    # Emits username and image to client
    # Emits the goals and progress
    
    user = db.session.query(models.Users).filter_by(email=data["email"]).first()

    if (not user):
        push_new_user_to_db(data['email'], data['username'], data['image'], "Null", data['id_token'])

    user = db.session.query(models.Users).filter_by(email=data["email"]).first()

    personal_profile = {
        "username": data["username"],
        "image": data["image"],
        "primary_id": user.id
    }

    personal_goals = [
        {
            "description": personal_goal.description,
            "progress": personal_goal.progress
        }
        for personal_goal in models.Goals.query.filter(models.Goals.user_id == user.id).all()
    ]


    server_socket.emit("google info received", personal_profile, request.sid)
    server_socket.emit("user goals", personal_goals, request.sid)



@server_socket.on('add_goal')
def add_goal(data):
    category = data["category"]
    user_id = data["users"]["primary_id"]
    description = data["goal"]
    progress = data["progress"]
    post_text = data["postText"]

    server_socket.emit("add_goal", data, request.sid)

    db.session.add(models.Goals(user_id, category, description, progress, post_text))
    db.session.commit()



def emit_google_info(channel):
    all_users = [{
        "username": user.name,
        "img_url": user.img_url,
        "user_id": user.id
        } for user in db.session.query(models.Users).all()]

    server_socket.emit(channel, {
        'allusers' : all_users
    })



@server_socket.on("connect")
def on_connect():
    emit_newsfeed(EMIT_EXERCISE_NEWSFEED_CHANNEL, request.sid)
    #emit_google_info(GOOGLE_INFO_RECEIVED_CHANNEL)



@app.route("/")
def index():
    """ Runs the app!!!"""
    return flask.render_template("index.html")


@app.route('/HomePage')
def HomePage():
    return flask.render_template("HomePage.html")

@app.route('/UserProfile')
def UserProfile():
    return flask.render_template("UserProfile.html")

@app.route('/AddGoal')
def AddGoal():
    return flask.render_template("AddGoal.html")

@app.route('/Art')
def Art():
    return flask.render_template("Art.html")



if __name__ == "__main__":
    server_socket.run(
        app,
        host=os.getenv("IP", "0.0.0.0"),
        port=int(os.getenv("PORT", 8080)),
        debug=True,
    )