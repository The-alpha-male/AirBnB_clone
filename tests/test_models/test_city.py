#!/usr/bin/python3
"""This module creates a City class"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.city import City


class TestCity_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the City class."""

    def test_no_args_instantiates(self):
        self.assertEqual(City, type(City()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(City(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(City().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(City().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(City().updated_at))

    def test_name_is_public_class_attribute(self):
        city = City()
        self.assertEqual(str, type(City.name))
        self.assertIn("name", dir(city))
        self.assertNotIn("name", city.__dict__)

    def test_state_id_is_public_class_attribute(self):
        city = City()
        self.assertEqual(str, type(City.state_id))
        self.assertIn("state_id", dir(city))
        self.assertNotIn("state_id", city.__dict__)

    def test_args_unused(self):
        self.assertNotIn("__init__", City.__dict__)

    def test_instantiation_with_no_kwargs(self):
        city = City()
        self.assertEqual(city.id, city.id)
        self.assertEqual(city.created_at, city.created_at)
        self.assertEqual(city.updated_at, city.updated_at)
        self.assertEqual(city.name, "")
        self.assertEqual(city.state_id, "")

    def test_instantiation_with_all_kwargs(self):
        time_format = "%Y-%m-%dT%H:%M:%S.%f"
        kwargs = {
            "id": "f7f99",
            "created_at": "2017-09-28T21:03:54.052298",
            "updated_at": "2017-09-28T21:03:54.052302",
            "name": "San Francisco",
            "state_id": "c7c99",
        }
        city = City(**kwargs)
        self.assertEqual(city.id, "f7f99")
        self.assertEqual(
            city.created_at, datetime.strptime
            (kwargs["created_at"], time_format)
        )
        self.assertEqual(
            city.updated_at, datetime.strptime
            (kwargs["updated_at"], time_format)
        )
        self.assertEqual(city.name, "San Francisco")
        self.assertEqual(city.state_id, "c7c99")

    def test_id_is_None(self):
        city = City()
        self.assertIsNone(city.id)

    def test_created_at_is_None(self):
        city = City()
        self.assertIsNone(city.created_at)

    def test_updated_at_is_None(self):
        city = City()
        self.assertIsNone(city.updated_at)

    class TestCity_to_dict(unittest.TestCase):
        """Unittests for testing to_dict method of the City class."""

        def test_to_dict_type(self):
            self.assertTrue(dict, type(City().to_dict()))

        def test_to_dict_contains_correct_keys(self):
            cy = City()
            self.assertIn("id", cy.to_dict())
            self.assertIn("created_at", cy.to_dict())
            self.assertIn("updated_at", cy.to_dict())
            self.assertIn("__class__", cy.to_dict())

        def test_to_dict_contains_added_attributes(self):
            cy = City()
            cy.middle_name = "Holberton"
            cy.my_number = 98
            self.assertEqual("Holberton", cy.middle_name)
            self.assertIn("my_number", cy.to_dict())

        def test_to_dict_datetime_attributes_are_strs(self):
            cy = City()
            cy_dict = cy.to_dict()
            self.assertEqual(str, type(cy_dict["id"]))
            self.assertEqual(str, type(cy_dict["created_at"]))
            self.assertEqual(str, type(cy_dict["updated_at"]))

        def test_to_dict_output(self):
            dt = datetime.today()
            cy = City()
            cy.id = "123456"
            cy.created_at = cy.updated_at = dt
            tdict = {
                "id": "123456",
                "__class__": "City",
                "created_at": dt.isoformat(),
                "updated_at": dt.isoformat(),
            }
            self.assertDictEqual(cy.to_dict(), tdict)

        def test_contrast_to_dict_dunder_dict(self):
            cy = City()
            self.assertNotEqual(cy.to_dict(), cy.__dict__)

        def test_to_dict_with_arg(self):
            cy = City()
            with self.assertRaises(TypeError):
                cy.to_dict(None)


if __name__ == "__main__":
    unittest.main()
