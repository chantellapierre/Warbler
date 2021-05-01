"""Message model tests."""

import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Message, Follows, Likes

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


from app import app
db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client"""
        db.drop_all()
        db.create_all()

        self.uid = 1
        u = User.signup(username="test",
                        email="test@test.com",
                        password="test",
                        image_url=None)
        u.id = self.uid
        db.session.commit()

        self.u = User.query.get(self.uid)

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_message_model(self):
        """Test model"""
        
        m = Message(
            text="test message",
            user_id=self.uid
        )
        db.session.add(m)
        db.session.commit()

       #Check if user received message
        self.assertEqual(len(self.u.messages), 1)
        self.assertEqual(self.u.messages[0].text, "test message")

    def test_message_likes(self):
        m1 = Message(
            text="test message",
            user_id=self.uid
        )

        m2 = Message(
            text="test message two",
            user_id=self.uid 
        )

        u = User.signup(username="test2",
                        email="test2@test.com",
                        password="test2",
                        image_url=None)
        uid = 2
        u.id = uid
        db.session.add_all([m1, m2, u])
        db.session.commit()

        u.likes.append(m1)
        db.session.commit()

        l = Likes.query.filter(Likes.user_id == uid).all()
        self.assertEqual(len(l), 1)
        self.assertEqual(l[0].message_id, m1.id)


        