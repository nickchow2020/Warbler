"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py

import os
from unittest import TestCase

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)

    def test_user_following(self):
        """Does the user following the correct user"""

        u1 = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        u2 = User(
            email="test@test1.com",
            username="testuser1",
            password="HASHED_PASSWORD"
        )

        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()

        follow1 = Follows(user_being_followed_id=u1.id,user_following_id=u2.id)
        db.session.add(follow1)
        db.session.commit()

        self.assertEqual(len(u2.following),1)
        self.assertEqual(len(u1.following),0)
        self.assertEqual(len(u1.followers),1)
        self.assertEqual(len(u2.followers),0)

    def test_create_user