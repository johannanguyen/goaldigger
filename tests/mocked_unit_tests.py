import unittest
import unittest.mock as mock
from os.path import join, dirname
from dotenv import load_dotenv
import sys
sys.path.insert(1, "../")
import flask_sqlalchemy
import requests
from flask import request
import flask_socketio
import app
from app import USERNAME_KEY, IMAGE_KEY, PRIMARY_ID_KEY, DESCRIPTION_KEY, PROGRESS_KEY
import models
from alchemy_mock.mocking import UnifiedAlchemyMagicMock

KEY_INPUT = "input"
KEY_EXPECTED = "expected"
KEY_CHANNEL = "channel"


class SocketNewsFeedTestCase(unittest.TestCase):
    ''' Test DB and Socket io functionality '''
    
    @mock.patch("app.flask.request.sid")
    def test_get_request_sid(self, mock_flask_request):
        """Testing request.sid"""
        mock_flask_request.sid = "mock_sid"
        res = app.get_request_sid()
        self.assertEqual(res, "mock_sid")
        
    # @mock.patch("app.flask")
    # def test_on_connect(self, mock_flask):
    #     mock_flask.request.sid = "mock sid"
    #     app.on_connect()
    
    @mock.patch("app.flask.request")
    @mock.patch("app.server_socket")
    @mock.patch("app.db")
    def test_add_goal(self, mocked_user_db, mocked_server_socket, mock_flask):
        ''' Testing new goal arrival '''
        d_goal = {
            "category" : "Test category",
            "users" : {"primary_id":"Test user id"},
            "goal" : "Test goal",
            "progress" : "Test progress",
            "postText" : "Test posttext",
        }
        expected_goals_model = models.Goals(d_goal["users"]["primary_id"],
                                            d_goal["category"],
                                            d_goal["goal"],
                                            d_goal["progress"],
                                            d_goal["postText"])
        app.add_goal(d_goal)
        mocked_user_db.session.add.assert_called_once()
        mocked_user_db.session.commit.assert_called_once()

        add_args, _ = mocked_user_db.session.add.call_args
        added_goals_model = add_args[0]
        
        mock_flask.request.sid = "mock_sid"
        res = app.get_request_sid()
        self.assertEqual(res, request.sid)

        self.assertEqual(added_goals_model.user_id, expected_goals_model.user_id)
        self.assertEqual(added_goals_model.category, expected_goals_model.category)
        self.assertEqual(added_goals_model.description, expected_goals_model.description)
        self.assertEqual(added_goals_model.progress, expected_goals_model.progress)
        self.assertEqual(added_goals_model.post_text, expected_goals_model.post_text)
        
        mocked_server_socket.emit.assert_called_once_with('add_goal', 
                                                        {'category': 'Test category', 
                                                        'users': {'primary_id': 'Test user id'}, 
                                                        'goal': 'Test goal', 
                                                        'progress': 'Test progress', 
                                                        'postText': 'Test posttext'},
                                                        request.sid)
                                                    
    # @mock.patch("app.server_socket")
    # def test_on_new_google_user(self, mocked_server_socket):
    #     # d_user = {'email': "foo@njit.edu", 
    #     #             'username': "test username", 
    #     #             'image': 'test img', 
    #     #             'is_signed_in': "Null", 
    #     #             'id_token': 'test id token'}
    #     d_user = {'email': "foo@njit.edu"}
    #     mocked_db_session = UnifiedAlchemyMagicMock()
    #     user = mocked_db_session.query(models.Users).filter_by(email=d_user["email"]).first()
    #     print("User before", user)
    #     if (not user):
    #         app.on_new_google_user(d_user)
    #         mocked_db_session.add.assert_called_once()
    #         mocked_db_session.commit.assert_called_once()
    #         add_args, _ = mocked_db_session.session.add.call_args
    #         added_user_model = add_args[0]
    #         print("Added user model", added_user_model)
            
    #     user = mocked_db_session.query(models.Users).filter_by(email=d_user['email']).first()
    #     print("User after", user)
        
    #     mock_personal_profile = {
    #         USERNAME_KEY: d_user["username"],
    #         IMAGE_KEY: d_user["image"],
    #         PRIMARY_ID_KEY: user.id,
    #     }
        
    #     mock_personal_goals = [{
    #         DESCRIPTION_KEY: mock_personal_goal.description,
    #         PROGRESS_KEY: mock_personal_goal.progress,
    #     } for mock_personal_goal in models.Goals.query.filter(models.Goals.user_id == user.id).all()
    #     ]
        
    #     mocked_server_socket.emit.assert_called_once_with('google info received', mock_personal_profile, request.sid)
    #     mocked_server_socket.emit.assert_called_once_with('user goals', mock_personal_profile, request.sid)
        
    # # @mock.patch("app.flask.request")
    # # @mock.patch("app.server_socket")
    # # @mock.patch("app.db")
    # # def test_emit_newsfeed(self, mocked_db, mocked_server_socket, mocked_flask_request):
        
        
    
if __name__ == "__main__":
    unittest.main()
        
        

        
            
            