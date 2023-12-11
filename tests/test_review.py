#!/usr/bin/python3
"""Defines unittests for models/review.py.

Unittest classes:
    TestReview_instantiation
    TestReview_save
    TestReview_to_dict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.review import Review


class TestReview_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the Review class."""

    def test_no_args_instantiates(self):
        self.assertEqual(Review, type(Review()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(Review(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(Review().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Review().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Review().updated_at))

    def test_place_id_is_public_class_attribute(self):
        review = Review()
        self.assertEqual(str, type(Review.place_id))
        self.assertIn("place_id", dir(review))
        self.assertNotIn("place_id", review.__dict__)

    def test_user_id_is_public_class_attribute(self):
        review = Review()
        self.assertEqual(str, type(Review.user_id))
        self.assertIn("user_id", dir(review))
        self.assertNotIn("user_id", review.__dict__)

    def test_text_is_public_class_attribute(self):
        review = Review()
        self.assertEqual(str, type(Review.text))
        self.assertIn("text", dir(review))
        self.assertNotIn("text", review.__dict__)

    def test_args_unused(self):
        self.assertNotIn("__init__", Review.__dict__)

    def test_instantiation_with_no_kwargs(self):
        review = Review()
        self.assertEqual(review.id, review.id)
        self.assertEqual(review.created_at, review.created_at)
        self.assertEqual(review.updated_at, review.updated_at)

    def test_instantiation_with_all_kwargs(self):
        kwargs = {
            "id": "56d43177-cc5f-4d6c-a0c1-e167f8c27337",
            "created_at": "2017-09-28T21:03:54.052298",
            "updated_at": "2017-09-28T21:03:54.052302",
            "place_id": "Place.1",
            "user_id": "User.1",
            "text": "Holberton School is awesome!",
        }
        review = Review(**kwargs)
        self.assertEqual(kwargs["id"], review.id)
        self.assertEqual(
            datetime.strptime(kwargs["created_at"], "%Y-%m-%dT%H:%M:%S.%f"),
            review.created_at,
        )
        self.assertEqual(
            datetime.strptime(kwargs["updated_at"], "%Y-%m-%dT%H:%M:%S.%f"),
            review.updated_at,
        )
        self.assertEqual(kwargs["place_id"], review.place_id)
        self.assertEqual(kwargs["user_id"], review.user_id)
        self.assertEqual(kwargs["text"], review.text)

    def test_instantiation_with_some_kwargs(self):
        kwargs = {
            "place_id": "Place.1",
            "user_id": "User.1",
            "text": "Holberton School is awesome!",
        }
        review = Review(**kwargs)
        self.assertNotEqual(kwargs["place_id"], review.id)
        self.assertNotEqual(kwargs["created_at"], review.created_at)
        self.assertNotEqual(kwargs["updated_at"], review.updated_at)
        self.assertEqual(kwargs["place_id"], review.place_id)
        self.assertEqual(kwargs["user_id"], review.user_id)
        self.assertEqual(kwargs["text"], review.text)

    def test_instantiation_with_None_kwargs(self):
        kwargs = {
            "id": None,
            "created_at": None,
            "updated_at": None,
            "place_id": None,
            "user_id": None,
            "text": None,
        }
        review = Review(**kwargs)
        self.assertNotEqual(kwargs["id"], review.id)
        self.assertNotEqual(kwargs["created_at"], review.created_at)
        self.assertNotEqual(kwargs["updated_at"], review.updated_at)
        self.assertEqual(kwargs["place_id"], review.place_id)
        self.assertEqual(kwargs["user_id"], review.user_id)
        self.assertEqual(kwargs["text"], review.text)

    def test_extra_kwargs(self):
        kwargs = {"text": "Holberton School is awesome!", "name": "Betty"}
        review = Review(**kwargs)
        self.assertNotIn("name", review.__dict__)
        self.assertIn("text", review.__dict__)


class TestReview_save(unittest.TestCase):
    """Unittests for testing save method of the Review class."""

    @classmethod
    def setUpClass(cls):
        cls.review = Review()
        cls.review.save()
        cls.updated_at = cls.review.updated_at
        sleep(0.1)
        cls.review.save()

    def test_save(self):
        self.assertNotEqual(self.review.updated_at, self.updated_at)

    def test_save_to_file(self):
        self.assertTrue(os.path.exists("file.json"))

    @classmethod
    def tearDownClass(cls):
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass

    def tear_down(self):
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass

    def test_save_no_args(self):
        with self.assertRaises(TypeError):
            self.review.save(None)

    def test_save_extra_args(self):
        with self.assertRaises(TypeError):
            self.review.save(None, None)

    def test_save_with_None(self):
        with self.assertRaises(TypeError):
            self.review.save(None)

    def test_save_with_two_args(self):
        with self.assertRaises(TypeError):
            self.review.save(None, None)

    def test_save_update_file(self):
        """Test that save updates the storage file"""
        from models import storage
        from models.base_model import BaseModel
        from models.review import Review
        from os import path
        import json
        import os

        bm1 = Review()
        bm1.save()
        bm1_id = "Review." + bm1.id
        storage.reload()
        self.assertEqual(storage.all()[bm1_id].to_dict(), bm1.to_dict())
        bm1.save()
        storage.reload()
        self.assertEqual(storage.all()[bm1_id].to_dict(), bm1.to_dict())
        with open("file.json", "r") as f:
            self.assertTrue(bm1_id in json.load(f).keys())
        os.remove("file.json")


class TestReview_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the Review class."""

    def test_to_dict(self):
        """Testing to_dict"""
        review = Review()
        review_dict = review.to_dict()
        self.assertEqual(dict, type(review_dict))
        self.assertIn("__class__", review_dict)
        self.assertEqual("Review", review_dict["__class__"])
        self.assertEqual(str, type(review_dict["id"]))
        self.assertEqual(review.id, review_dict["id"])
        self.assertEqual(datetime, type(review_dict["created_at"]))
        self.assertEqual(review.created_at.isoformat(), review_dict["created_at"])
        self.assertEqual(datetime, type(review_dict["updated_at"]))
        self.assertEqual(review.updated_at.isoformat(), review_dict["updated_at"])
        self.assertEqual(str, type(review_dict["place_id"]))
        self.assertEqual(review.place_id, review_dict["place_id"])
        self.assertEqual(str, type(review_dict["user_id"]))
        self.assertEqual(review.user_id, review_dict["user_id"])
        self.assertEqual(str, type(review_dict["text"]))
        self.assertEqual(review.text, review_dict["text"])

    def test_to_dict_no_args(self):
        """Testing to_dict with no arguments"""
        with self.assertRaises(TypeError):
            Review.to_dict()

    def test_to_dict_extra_args(self):
        """Testing to_dict with extra arguments"""
        with self.assertRaises(TypeError):
            Review.to_dict(None)

    def test_to_dict_one_arg(self):
        """Testing to_dict with one argument"""
        with self.assertRaises(TypeError):
            Review.to_dict("Betty")

    def test_to_dict_two_args(self):
        """Testing to_dict with two arguments"""
        with self.assertRaises(TypeError):
            Review.to_dict("Betty", "Holberton")

    def test_to_dict_update(self):
        """Test that to_dict updates storage file"""
        from models import storage
        from models.base_model import BaseModel
        from models.review import Review
        from os import path
        import json
        import os

        bm1 = Review()
        bm1_dict = bm1.to_dict()
        bm1.save()
        bm1_id = "Review." + bm1.id
        storage.reload()
        self.assertEqual(storage.all()[bm1_id].to_dict(), bm1.to_dict())
        bm1.save()
        storage.reload()
        self.assertEqual(storage.all()[bm1_id].to_dict(), bm1.to_dict())
        with open("file.json", "r") as f:
            self.assertTrue(bm1_id in json.load(f).keys())
        os.remove("file.json")


if __name__ == "__main__":
    unittest.main()
