import os
import flask
from flask import Flask, render_template
import flask_socketio
import flask_sqlalchemy
from dotenv import load_dotenv
from os.path import join, dirname
import requests
from flask import request


app = Flask(__name__)
server_socket = flask_socketio.SocketIO(app)
server_socket.init_app(app, cors_allowed_origins="*")

EMIT_ALL_GOALS_CHANNEL = "goal_history"

DOTENV_PATH = join(dirname(__file__), "sql.env")
load_dotenv(DOTENV_PATH)

DATABASE_URI = os.environ["DATABASE_URL"]

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI

db = flask_sqlalchemy.SQLAlchemy(app)
db.app = app

db.create_all()
db.session.commit()

import models

NUM_USERS = 0

def emit_all_goals(channel):
    """Emits all contents of the database to newest client"""
    all_names = [
        DB_name.name
        for DB_name in db.session.query(models.FakeTable).all()
    ]

    all_images = [
        DB_image.image
        for DB_image in db.session.query(models.FakeTable).all()
    ]
    
    all_goals = [
        DB_goal.goal
        for DB_goal in db.session.query(models.FakeTable).all()
    ]

    all_statuses = [
        DB_status.status
        for DB_status in db.session.query(models.FakeTable).all()
    ]
    
    all_messages = [
        DB_message.message
        for DB_message in db.session.query(models.FakeTable).all()
    ]

    server_socket.emit(channel,
        {
            "all_names": all_names,
            "all_images": all_images,
            "all_goals": all_goals,
            "all_statuses": all_statuses,
            "all_messages": all_messages,

        }, broadcast=True
    )
    print("ALL NAMES: ", all_names)
    print("ALL IMAGES: ", all_images)
    print("ALL GOALS: ", all_goals)
    print("ALL STATUSES: ", all_statuses)
    print("ALL MESSAGES: ", all_messages)
    

@server_socket.on("connect")
def on_connect():
   emit_all_goals(EMIT_ALL_GOALS_CHANNEL)


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
