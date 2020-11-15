""" Testing all db and socket functionality from app.py """
import unittest.mock as mock
import unittest
import sys
sys.path.insert(1, "../")
from alchemy_mock.mocking import UnifiedAlchemyMagicMock
import app
from app import USERNAME_KEY, IMAGE_KEY, PRIMARY_ID_KEY
from app import EMIT_EXERCISE_NEWSFEED_CHANNEL
from app import (
    ALL_IDS_KEY,
    ALL_NAMES_KEY,
    ALL_IMAGES_KEY,
    ALL_CATEGORIES_KEY,
    ALL_USER_PRIMARY_IDS_KEY,
    ALL_DESCRIPTIONS_KEY,
    ALL_PROGRESS_KEY,
    ALL_POST_TEXTS_KEY,
)
import models

KEY_INPUT = "input"
KEY_EXPECTED = "expected"
KEY_CHANNEL = "channel"


class SocketNewsFeedTestCase(unittest.TestCase):
    """ Test DB and Socket io functionality """

    @mock.patch("app.flask.request")
    def test_get_request_sid(self, mock_flask_request):
        """ Testing request.sid """
        mock_flask_request.sid = "mock_sid"
        res = app.get_request_sid()
        self.assertEqual(res, "mock_sid")

    @mock.patch("app.flask")
    def test_on_connect(self, mock_flask):
        """ Testing on connect """
        mock_flask.request.sid = "mock sid"
        app.on_connect()

    @mock.patch("app.server_socket")
    @mock.patch("app.db")
    def test_add_goal(self, mocked_db, mocked_server_socket):
        """ Testing new goal arrival """
        d_goal = {
            "category": "Test category",
            "users": {"primary_id": "Test user id"},
            "goal": "Test goal",
            "progress": "Test progress",
            "postText": "Test posttext",
        }
        expected_goals_model = models.Goals(
            d_goal["users"]["primary_id"],
            d_goal["category"],
            d_goal["goal"],
            d_goal["progress"],
            d_goal["postText"],
        )
        app.add_goal(d_goal)
        mocked_db.session.add.assert_called_once()
        mocked_db.session.commit.assert_called_once()

        add_args, _ = mocked_db.session.add.call_args
        added_goals_model = add_args[0]
        # mock_user_id = mocked_db.session.query().filter_by().first().id

        self.assertEqual(added_goals_model.user_id, expected_goals_model.user_id)
        self.assertEqual(added_goals_model.category, expected_goals_model.category)
        self.assertEqual(
            added_goals_model.description, expected_goals_model.description
        )
        self.assertEqual(added_goals_model.progress, expected_goals_model.progress)
        self.assertEqual(added_goals_model.post_text, expected_goals_model.post_text)

        mocked_server_socket.emit.assert_called_once_with(
            "add_goal",
            {
                "category": "Test category",
                "users": {"primary_id": "Test user id"},
                "goal": "Test goal",
                "progress": "Test progress",
                "postText": "Test posttext",
            },
        )

    @mock.patch("app.server_socket")
    @mock.patch("app.db")
    def test_on_new_google_user(self, mocked_db, mocked_server_socket):
        """Testing new google user arrival"""

        d_user = {
            "email": "test@njit.edu",
            "username": "test username",
            "image": "test img",
            "is_signed_in": "Null",
            "id_token": "test id token",
        }

        expected_user_model = models.Users(
            d_user["email"],
            d_user["username"],
            d_user["image"],
            "Null",
            d_user["id_token"],
        )

        session = UnifiedAlchemyMagicMock()
        user = session.query(models.Users).filter_by(email=d_user["email"]).first()
        # user = mocked_db.session.query(models.Users).filter_by(email=d_user['email']).first()
        if not user:
            app.on_new_google_user(d_user)
            mocked_db.session.add.assert_called_once()
            mocked_db.session.commit.assert_called_once()
            add_args, _ = mocked_db.session.add.call_args
            added_user_model = add_args

        user = added_user_model[1]
        mock_id = mocked_db.session.query().filter_by().first().id

        self.assertEqual(added_user_model[0], expected_user_model.email)
        self.assertEqual(added_user_model[1], expected_user_model.name)
        self.assertEqual(added_user_model[2], expected_user_model.img_url)
        self.assertEqual(added_user_model[3], expected_user_model.signed_in)
        self.assertEqual(added_user_model[4], expected_user_model.google_id)

        mock_personal_profile = {
            USERNAME_KEY: d_user["username"],
            IMAGE_KEY: d_user["image"],
            PRIMARY_ID_KEY: mock_id,
        }

        # mock_personal_goals = [{
        #     DESCRIPTION_KEY: mock_personal_goal.description,
        #     PROGRESS_KEY: mock_personal_goal.progress,
        # } for mock_personal_goal in mocked_db.models.Goals.query.filter(mocked_user_id == user.id).all()
        # ]

        mocked_server_socket.emit.assert_called_once_with(
            "google info received", mock_personal_profile
        )
        # mocked_server_socket.emit.assert_called_once_with('user goals', mock_personal_goals)

    @mock.patch("app.server_socket")
    @mock.patch("app.db")
    def test_emit_newsfeed(self, mocked_db, mocked_server_socket):
        """ Testing emitting newsfeed """
        mock_all_ids = [
            mock_DB_id.id for mock_DB_id in mocked_db.session.query(models.Users).all()
        ]
        mock_all_names = [
            mock_DB_name.name
            for mock_DB_name in mocked_db.session.query(models.Users).all()
        ]
        mock_all_images = [
            mock_DB_img_url.img_url
            for mock_DB_img_url in mocked_db.session.query(models.Users).all()
        ]
        mock_all_categories = [
            mock_DB_category.category
            for mock_DB_category in mocked_db.session.query(models.Goals).all()
        ]

        mock_all_user_primary_ids = [
            mock_DB_user_primary_id.user_id
            for mock_DB_user_primary_id in mocked_db.session.query(models.Goals).all()
        ]

        mock_all_descriptions = [
            mock_DB_description.description
            for mock_DB_description in mocked_db.session.query(models.Goals).all()
        ]

        mock_all_progress = [
            mock_DB_progress.progress
            for mock_DB_progress in mocked_db.session.query(models.Goals).all()
        ]

        mock_all_post_texts = [
            mock_DB_post_text.post_text
            for mock_DB_post_text in mocked_db.session.query(models.Goals).all()
        ]

        for mocked_db_users, mocked_db_goals in (
            mocked_db.session.query(models.Users, models.Goals)
            .filter(models.Users.id == models.Goals.user_id)
            .order_by(models.Goals.date)
            .all()
        ):
            mock_all_ids.append(mocked_db_users.id)
            mock_all_names.append(mocked_db_users.name)
            mock_all_images.append(mocked_db_users.img_url)
            mock_all_categories.append(mocked_db_goals.category)
            mock_all_descriptions.append(mocked_db_goals.description)
            mock_all_progress.append(mocked_db_goals.progress)

        app.emit_newsfeed(EMIT_EXERCISE_NEWSFEED_CHANNEL)
        mocked_server_socket.emit.assert_called_once_with(
            EMIT_EXERCISE_NEWSFEED_CHANNEL,
            {
                ALL_IDS_KEY: mock_all_ids,
                ALL_NAMES_KEY: mock_all_names,
                ALL_IMAGES_KEY: mock_all_images,
                ALL_CATEGORIES_KEY: mock_all_categories,
                ALL_USER_PRIMARY_IDS_KEY: mock_all_user_primary_ids,
                ALL_DESCRIPTIONS_KEY: mock_all_descriptions,
                ALL_PROGRESS_KEY: mock_all_progress,
                ALL_POST_TEXTS_KEY: mock_all_post_texts,
            },
        )


if __name__ == "__main__":
    unittest.main()
