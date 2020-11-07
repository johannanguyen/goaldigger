import os
from os.path import join, dirname
import flask
from flask import Flask, render_template
import flask_socketio
import flask_sqlalchemy
from dotenv import load_dotenv
from google.auth.transport import requests
from google.oauth2 import id_token as idToken
from flask import request as Request
import models


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
    

NUM_USERS = 0

@server_socket.on("connect")
def on_connect():
    global NUM_USERS
    NUM_USERS += 1
    
    print("Someone connected!", NUM_USERS)
    server_socket.emit("new_user", NUM_USERS, broadcast=True)
    
    
@server_socket.on("google_user")
def on_google_user(data):
    """Grabs Google data and processes its elements accordingly"""

    print("Google user data:", data)
    name = data["name"]
    google_id = data["google_id"]
    image = data["image"]
    is_signed_in = data["is_signed_in"]

    if is_signed_in:
        server_socket.emit(
            "new_user",
            {
                "name": name,
                "google_id": google_id, 
                "image": image
            },
            Request.sid,
        )


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
