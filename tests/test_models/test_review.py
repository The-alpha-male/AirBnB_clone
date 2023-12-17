#!/usr/bin/python3
"""Unit Testings for review class"""

import unittest
import models
from models.review import Review
from datetime import datetime
from time import sleep
import os


class Test_Review(unittest.TestingCase):
    """Testing casess for Review class"""

    def setUp(self):
        """Set up the env before each Testing case"""
        self.review = Review()

    def tearDown(self):
        """Clean up the Testing env after each Testing case if needed"""
        self.review = None

    def Test_init_with_arguments(self):
        """Testing initialization with arguments"""
        data = {
            'id': '1234',
            'created_at': '2023-12-01T00:00:00',
            'updated_at': '2023-12-01T00:00:00',
            'name': 'Testing'
        }
        self.review = Review(**data)

        # Verify that the attributes are set correctly
        self.assertEqual(self.review.id, '1234')
        self.assertEqual(self.review.created_at,
                         datetime.fromisoformat('2023-12-01T00:00:00'))
        self.assertEqual(self.review.updated_at,
                         datetime.fromisoformat('2023-12-01T00:00:00'))
        self.assertEqual(self.review.name, 'Testing')

    def Test_init_without_arguments(self):
        """Testing initialization without arguments"""
        self.review = Review()

        # Verify that the attributes are set correctly
        self.assertIsNotNone(self.review.id)
        self.assertIsNotNone(self.review.created_at)
        self.assertIsNotNone(self.review.updated_at)
        self.assertEqual(self.review.created_at, self.review.updated_at)

    def Test_args(self):
        """Testinging args which was unused"""
        rv = Review(None)
        self.assertNotIn(None, rv.__dict__.values())

    def Test_with_kwargs(self):
        """Testinging with kwargs"""
        date = datetime.now()
        tform = date.isoformat()
        rv = Review(id="1234", created_at=tform, updated_at=tform)
        self.assertEqual(rv.id, "1234")
        self.assertEqual(rv.created_at, date)
        self.assertEqual(rv.updated_at, date)

    def Test_kwargs_None(self):
        """Testinging with kwargs at None"""
        with self.assertRaises(TypeError):
            Review(id=None, created_at=None, updated_at=None)

    def Test_with_args_and_kwargs(self):
        """ Testinging with both args and kwargs"""
        date = datetime.now()
        tform = date.isoformat()
        rv = Review(id="1234", created_at=tform, updated_at=tform)
        self.assertEqual(rv.id, "1234")
        self.assertEqual(rv.created_at, date)
        self.assertEqual(rv.updated_at, date)

    def Test_attributes_initialization(self):
        """Testing attr initialization"""
        self.assertEqual(self.review.place_id, "")
        self.assertEqual(self.review.user_id, "")
        self.assertEqual(self.review.text, "")
        self.assertTrue(hasattr(self.review, "id"))
        self.assertTrue(hasattr(self.review, "created_at"))
        self.assertTrue(hasattr(self.review, "updated_at"))

    def Test_id_is_str(self):
        """checks if id data type"""
        self.assertEqual(str, type(Review().id))

    def Test_id_is_unique(self):
        """Testing if ids generated are unique"""
        user1 = Review()
        user2 = Review()
        self.assertNotEqual(user1.id, user2.id)

    def Test_created_at_datetime(self):
        """Checks if the attribute is a datetime object"""
        self.assertEqual(datetime, type(Review().created_at))

    def Test_created_at_timestamp(self):
        """checks if the timestamp is different"""
        user1 = Review()
        sleep(0.05)
        user2 = Review()
        self.assertLess(user1.created_at, user2.created_at)

    def Test_updated_at_datetime(self):
        """Checks if attribute is a datetime object"""
        self.assertEqual(datetime, type(Review(). updated_at))

    def Test_updated_at_timestamp(self):
        """Checks if the timestamp is different"""
        user1 = Review()
        sleep(0.05)
        user2 = Review()
        self.assertLess(user1.updated_at, user2.updated_at)

    def Test_instance_storage(self):
        """checks if storage and retrival were successful"""
        self.assertIn(Review(), models.storage.all().values())

    def Test__str__(self):
        """Testings the string representation"""
        rv1 = Review()
        rv2 = Review()
        self.assertNotEqual(rv1.__str__(), rv2.__str__())

    def Test__str__method(self):
        """Testings the str() method"""
        rv_str = str(self.review)
        self.assertIn("[Review]", rv_str)
        self.assertIn("id", rv_str)
        self.assertIn("created_at", rv_str)
        self.assertIn("updated_at", rv_str)

    def Test_save(self):
        """Testings the effectivity of timestamp updates"""
        rv = Review()
        sleep(0.1)
        update = rv.updated_at
        rv.save()
        self.assertLess(update, rv.updated_at)

    def Test_two_saves(self):
        """Testings the effectivity of different timestamps updates"""
        rv = Review()
        sleep(0.1)
        update1 = rv.updated_at
        rv.save()
        update2 = rv.updated_at
        self.assertLess(update1, update2)
        sleep(0.1)
        rv.save()
        self.assertLess(update2, rv.updated_at)

    def Test_save_updates_file(self):
        """Testings that updates are updated and stored correctly"""
        rv = Review()
        rv.save()
        rvid = "Review." + rv.id
        with open("file.json", "r") as file:
            self.assertIn(rvid, file.read())

    def Test_save_method(self):
        """Testings the save() method"""
        updated_at_1 = self.review.updated_at
        self.review.save()
        updated_at_2 = self.review.updated_at
        self.assertNotEqual(updated_at_1, updated_at_2)

    def Test_to_dict(self):
        """Testings the expected output"""
        expected_dict = {
            'id': self.review.id,
            'created_at': self.review.created_at.isoformat(),
            'updated_at': self.review.updated_at.isoformat(),
            '__class__': 'Review'
        }
        self.assertEqual(self.review.to_dict(), expected_dict)

    def Test_to_dict_type(self):
        """verifys the class returns a dictionary"""
        rv = Review()
        self.assertTrue(dict, type(rv.to_dict()))

    def Test_different_to_dict(self):
        """Testings that the class produces 2 diff dict for diff instances"""
        rv1 = Review()
        sleep(0.05)
        rv2 = Review()
        self.assertNotEqual(rv1.to_dict(), rv2.to_dict())

    def Test_to_dict_has_correct_keys(self):
        """Testings that the dict contains the right keys"""
        rv = Review()
        self.assertIn("id", rv.to_dict())
        self.assertIn("__class__", rv.to_dict())
        self.assertIn("created_at", rv.to_dict())
        self.assertIn("updated_at", rv.to_dict())

    def Test_to_dict_created_at_format(self):
        """checks the ISO formatted string"""
        rv = self.review.to_dict()
        created_at = rv["created_at"]
        self.assertEqual(created_at, self.review.created_at.isoformat())

    def Test_to_dict_updated_at_format(self):
        """checks the ISO formatted string"""
        rv = self.review.to_dict()
        updated_at = rv["updated_at"]
        self.assertEqual(updated_at, self.review.updated_at.isoformat())


if __name__ == "__main__":
    unittest.main()
