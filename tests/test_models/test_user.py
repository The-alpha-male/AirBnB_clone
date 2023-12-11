#!/usr/bin/python3

"""Unittest for user class"""

from datetime import datetime
from models.user import User
import models
import os
import unittest


class TestUser(unittest.TestCase):
    """Test case for User class"""

    def setUp(self):
        """Set up env before test case"""
        self.user = User()

    def tearDown(self):
        """Clean test env after each testcase if needed"""
        del self.user

    def test_instance_created(self):
        """Tests if an instance was created correctly"""
        self.assertIsInstance(self.user, User)

    def test_init_args(self):
        """Test init with args"""
        data = {
            'id': '1234'
            'created_at': '2023-12-01T00:00:00',
            'updated_at': '2023-12-01T00:00:00',
            'name': 'Testing'
        }
        self.user = User(**data)

        """Verify that attributes are set correctly"""
        self.assertEqual(self.user.id, '1234')
        self.assertEqual(self.user.created_at,
                         datetime.fromisoformat('2023-12-01T00:00:00'))
        self.assertEqual(self.user.updated_at,
                         datetime.fromisoformat('2023-12-01T00:00:00'))
        self.assertEqual(self.user.name, 'Testing')

    def test_init_without_args(self):
        """Testing init without args"""
        self.user = User()

        """Verify attributes are set correctly"""
        self.assertIsNotNone(self.user.id)
        self.assertIsNotNone(self.user.created_at)
        self.assertIsNotNone(self.user.updated_at)
        self.assertIsNotNone(self.user.name)
        self.assertEqual(self.user.created_at, self.user.updated_at)

    def test_kwargs(self):
        """Testing kwargs"""
        date = datetime.now()
        tform = date.isoformat()
        usr = User(id='1234', created_at=tform, updated_at=tform)
        self.assertEqual(usr.id, '1234')
        self.assertEqual(usr.created_at, date)
        self.assertEqual(usr.updated_at, date)

    def test_missing_kwargs(self):
        """Tests if Kwargs are missing"""
        with self.assertRaises(TypeError):
            User(id=None, name=None, email=None, password=None)

    def test_args_and_kwargs(self):
        """Test both args and kwargs"""
        date = datetime.datetime.now()
        tform = date.isoformat()
        usr = User(id='1234', created_at=tform.updated_at=tform)
        self.assertEqual(usr.id, '1234')
        self.assertEqual(usr.created_at, date)
        self.assertEqual(usr.updated_at, date)

    def test_attributes(self):
        """tests the attributes for class user"""
        self.assertTrue(hasattr(self.user, "email"))
        self.assertTrue(hasattr(self.user, "password"))
        self.assertTrue(hasattr(self.user, "first_name"))
        self.assertTrue(hasattr(self.user, "last_name"))

    def test_attributes_default_values(self):
        """test default values of attributes"""
        self.assertEqual(self.user.email, "")
        self.assertEqual(self.user.password, "")
        self.assertEqual(self.user.first_name, "")
        self.assertEqual(self.user.last_name, "")

    def test_id_str(self):
        """Tests if id is string"""
        self.assertEqual(str, type(User().id))

    def test_unique_id(self):
        """Test if id generated is unique"""
        user1 = User()
        user2 = User()
        self.assertNotEqual(user1.id, user2.id)

    def test_created_at_datetime(self):
        """Checks if the attribute is a datetime object"""
        self.assertEqual(datetime, type(User().created_at))

    def test_created_at_timestamp(self):
        """checks if the timestamp is different"""
        user1 = User()
        sleep(0.05)
        user2 = User()
        self.assertLess(user1.created_at, user2.created_at)

    def test_instance_storage(self):
        """checks if storage and retrival were successful"""
        self.assertIn(User(), models.storage.all().values())

    def test_to_dict(self):
        """Tests the expected output"""
        expected_dict = {
            'id': self.user.id,
            'created_at': self.user.created_at.isoformat(),
            'updated_at': self.user.updated_at.isoformat(),
            '__class__': 'User'
        }
        self.assertEqual(self.user.to_dict(), expected_dict)

    def test_to_dict_type(self):
        """verifys the class returns a dictionary"""
        usr = User()
        self.assertTrue(dict, type(usr.to_dict()))

    def test_different_to_dict(self):
        """tests that the class produces 2 diff dict for diff instances"""
        usr1 = User()
        sleep(0.05)
        usr2 = User()
        self.assertNotEqual(usr1.to_dict(), usr2.to_dict())

    def test_to_dict_has_correct_keys(self):
        """tests that the dict contains the right keys"""
        usr = User()
        self.assertIn("id", usr.to_dict())
        self.assertIn("__class__", usr.to_dict())
        self.assertIn("created_at", usr.to_dict())
        self.assertIn("updated_at", usr.to_dict())

    def test_to_dict_created_at_format(self):
        """checks the ISO formatted string"""
        usr = self.user.to_dict()
        created_at = usr["created_at"]
        self.assertEqual(created_at, self.user.created_at.isoformat())


if __name__ == "__main__":
    unittest.main()
