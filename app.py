""" Main app.py """
import os
from os.path import join, dirname
import flask
import flask_socketio
import flask_sqlalchemy
from dotenv import load_dotenv

app = flask.Flask(__name__)

dotenv_path = join(dirname(__file__), "sql.env")
load_dotenv(dotenv_path)
database_uri = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_DATABASE_URI"] = database_uri

server_socket = flask_socketio.SocketIO(app)
server_socket.init_app(app, cors_allowed_origins="*")

db = flask_sqlalchemy.SQLAlchemy(app)
db.init_app(app)
db.app = app

db.create_all()
db.session.commit()

import models


EMIT_EXERCISE_NEWSFEED_CHANNEL = "homepage"
GOOGLE_INFO_RECEIVED_CHANNEL = "google info received"
ALL_IDS_KEY = "all_ids"
ALL_NAMES_KEY = "all_names"
ALL_IMAGES_KEY = "all_images"
ALL_CATEGORIES_KEY = "all_categories"
ALL_USER_PRIMARY_IDS_KEY = "all_user_primary_ids"
ALL_DESCRIPTIONS_KEY = "all_descriptions"
ALL_PROGRESS_KEY = "all_progress"
ALL_POST_TEXTS_KEY = "all_post_texts"
USERNAME_KEY = "username"
IMAGE_KEY = "image"
PRIMARY_ID_KEY = "primary_id"
DESCRIPTION_KEY = "description"
PROGRESS_KEY = "progress"


def emit_newsfeed(channel):
    """ function that emits user and goal info to newsfeed """
    all_ids = [DB_id.id for DB_id in db.session.query(models.Users).all()]
    all_names = [DB_name.name for DB_name in db.session.query(models.Users).all()]

    all_images = [
        DB_img_url.img_url for DB_img_url in db.session.query(models.Users).all()
    ]
    """
    all_goal_ids = [
        DB_id.id
        for DB_id in db.session.query(models.Goals).all()
    ]
    """
    all_categories = [
        DB_category.category for DB_category in db.session.query(models.Goals).all()
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
        DB_progress.progress for DB_progress in db.session.query(models.Goals).all()
    ]

    all_post_texts = [
        DB_post_text.post_text for DB_post_text in db.session.query(models.Goals).all()
    ]

    for db_users, db_goals in (
        db.session.query(models.Users, models.Goals)
        .filter(models.Users.id == models.Goals.user_id)
        .order_by(models.Goals.date)
        .all()
    ):
        all_ids.append(db_users.id)
        all_names.append(db_users.name)
        all_images.append(db_users.img_url)
        all_categories.append(db_goals.category)
        all_descriptions.append(db_goals.description)
        all_progress.append(db_goals.progress)

    server_socket.emit(
        channel,
        {
            ALL_IDS_KEY: all_ids,
            ALL_NAMES_KEY: all_names,
            ALL_IMAGES_KEY: all_images,
            # "all_goal_ids": all_goal_ids,
            ALL_CATEGORIES_KEY: all_categories,
            ALL_USER_PRIMARY_IDS_KEY: all_user_primary_ids,
            ALL_DESCRIPTIONS_KEY: all_descriptions,
            ALL_PROGRESS_KEY: all_progress,
            # "all_dates": all_dates,
            ALL_POST_TEXTS_KEY: all_post_texts,
        },
    )


def get_request_sid():
    """ returns request.sid """
    return flask.request.sid


@server_socket.on("new google user")
def on_new_google_user(data):
    """Grabs all of the users CURRENTLY in the database
    Grabs the new google login email and checks to see if it is in the list of emails
    If it is not, it will add that user to the database
    The email array will have to be repopulated (to account for newly added user)
    primary_id is determined by taking the index of where the email is located in the email array + 1
    example:
        all_emails = [johanna@gmail.com, joey@gmail.com]
        johanna's primary id = 0 + 1 = 1
    Grabs all the goals and progress in the database relating to the primary id
    Emits username and image to client
    Emits the goals and progress"""
    email = data["email"]
    username = data["username"]
    image = data["image"]
    id_token = data["id_token"]

    user = db.session.query(models.Users).filter_by(email=data["email"]).first()

    if not user:
        db.session.add(
            data["email"], data["username"], data["image"], "Null", data["id_token"]
        )
        db.session.commit()
    db.session.add(email, username, image, "Null", id_token)
    db.session.commit()

    user = db.session.query(models.Users).filter_by(email=data["email"]).first()

    personal_profile = {
        USERNAME_KEY: data["username"],
        IMAGE_KEY: data["image"],
        PRIMARY_ID_KEY: user.id,
    }

    """
    personal_goals = [
        {
            DESCRIPTION_KEY: personal_goal.description,
            PROGRESS_KEY: personal_goal.progress
        }
        for personal_goal in models.Goals.query.filter(models.Goals.user_id == user.id).all()
    ]
    server_socket.emit("user goals", personal_goals)
    """
    server_socket.emit("google info received", personal_profile)


@server_socket.on("add_goal")
def add_goal(data):
    """ receive goal from client and add it"""
    category = data["category"]
    user_id = data["users"]["primary_id"]
    description = data["goal"]
    progress = data["progress"]
    post_text = data["postText"]

    db.session.add(models.Goals(user_id, category, description, progress, post_text))
    db.session.commit()

    server_socket.emit("add_goal", data)


@server_socket.on("connect")
def on_connect():
    """ emit newsfeed on connect """
    print("Connected")
    emit_newsfeed(EMIT_EXERCISE_NEWSFEED_CHANNEL)


@app.route("/")
def index():
    """ Runs the app!!!"""
    return flask.render_template("index.html")


@app.route("/HomePage")
def home_page():
    """ render homepage """
    return flask.render_template("HomePage.html")


@app.route("/UserProfile")
def user_profile():
    """ render user profile """
    return flask.render_template("UserProfile.html")


@app.route("/AddGoal")
def add_goal_page():
    """ render add goal """
    return flask.render_template("AddGoal.html")


@app.route("/Art")
def art_page():
    """ render art page"""
    return flask.render_template("Art.html")


if __name__ == "__main__":
    server_socket.run(
        app,
        host=os.getenv("IP", "0.0.0.0"),
        port=int(os.getenv("PORT", 8080)),
        debug=True,
    )
