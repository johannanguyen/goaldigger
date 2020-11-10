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


app = Flask(__name__)
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
    all_ids = [
        DB_id.id
        for DB_id in db.session.query(models.Users).all()
    ]
    all_names = [
        DB_name.name
        for DB_name in db.session.query(models.Users).all()
    ]


    all_images = [
        DB_img_url.img_url
        for DB_img_url in db.session.query(models.Users).all()
    ]
    """
    all_goal_ids = [
        DB_id.id
        for DB_id in db.session.query(models.Goals).all()
    ]
    """
    all_categories = [
        DB_category.category
        for DB_category in db.session.query(models.Goals).all()
    ]
    
    all_user_primary_ids = [
        DB_user_primary_id.user_id
        for DB_user_primary_id in db.session.query(models.Goals).all()
    ]

    
    all_descriptions = [
        DB_description.description
        for DB_description in db.session.query(models.Goals).all()
    ]
    
    all_progress = [
        DB_progress.progress
        for DB_progress in db.session.query(models.Goals).all()
    ]
    
    all_post_texts = [
        DB_post_text.post_text
        for DB_post_text in db.session.query(models.Goals).all()
    ]

    for db_users, db_goals in db.session.query(models.Users, models.Goals).filter(models.Users.id == models.Goals.user_id).order_by(models.Goals.date).all():
        all_ids.append(db_users.id)
        all_names.append(db_users.name)
        all_images.append(db_users.img_url)
        all_categories.append(db_goals.category)
        all_descriptions.append(db_goals.description)
        all_progress.append(db_goals.progress)
    
    server_socket.emit(
        channel,
        {
            "all_ids": all_ids,
            "all_names": all_names,
            "all_images": all_images,
            #"all_goal_ids": all_goal_ids,
            "all_categories": all_categories,
            "all_user_primary_ids": all_user_primary_ids,
            "all_descriptions": all_descriptions,
            "all_progress": all_progress,
            #"all_dates": all_dates,
            "all_post_texts": all_post_texts
        },
        sid,
    )
    print(all_ids, all_names, all_images)
    


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
    
    all_emails = [
        DB_email.email
        for DB_email in db.session.query(models.Users).all()
    ]
    
    if (not data["email"] in all_emails):
        push_new_user_to_db(data['email'], data['username'], data['image'], data['is_signed_in'], data['id_token'])
        
    all_emails = [
        DB_email.email
        for DB_email in db.session.query(models.Users).all()
    ]

    primary_id = all_emails.index(data["email"]) + 1
    
    personal_profile = {
        "username": data["username"],
        "image": data["image"],
        "primary_id": primary_id
    }
    
    personal_goals = [
        personal_goal.description
        for personal_goal in models.Goals.query.filter(models.Goals.user_id == primary_id) 
    ]
    
    personal_progress = [
        personal_progress.progress
        for personal_progress in models.Goals.query.filter(models.Goals.user_id == primary_id)
    ]
    
    server_socket.emit("google info received", personal_profile, request.sid)
    server_socket.emit("goal_description", personal_goals, request.sid)
    server_socket.emit("goal_progress", personal_progress, request.sid)
   
    
    
@server_socket.on('add_goal')
def add_goal(data):
    category = data["category"]
    user_id = data["users"]["primary_id"]
    description = data["goal"]
    progress = data["progress"]
    post_text = data["postText"]
    
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



@app.route("/", methods=["GET", "POST"])
def hello():
    """ Runs the app!!!"""
    return flask.render_template("index.html")



if __name__ == "__main__":
    server_socket.run(
        app,
        host=os.getenv("IP", "0.0.0.0"),
        port=int(os.getenv("PORT", 8080)),
        debug=True,
    )