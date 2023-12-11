#!/usr/bin/python3
"""This module tests the State class"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.state import State


class TestState_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the State class."""

    def test_no_args_instantiates(self):
        self.assertEqual(State, type(State()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(State(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(State().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(State().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(State().updated_at))

    def test_name_is_public_class_attribute(self):
        state = State()
        self.assertEqual(str, type(State.name))
        self.assertIn("name", dir(state))
        self.assertNotIn("name", state.__dict__)

    def test_args_unused(self):
        self.assertNotIn("__init__", State.__dict__)

    def test_instantiation_with_no_kwargs(self):
        state = State()
        self.assertEqual(state.id, state.id)
        self.assertEqual(state.created_at, state.created_at)
        self.assertEqual(state.updated_at, state.updated_at)
        self.assertEqual(state.name, "")

    def test_instantiation_with_all_kwargs(self):
        time_format = "%Y-%m-%dT%H:%M:%S.%f"
        kwargs = {
            "id": "f7f99",
            "created_at": "2017-09-28T21:03:54.052298",
            "updated_at": "2017-09-28T21:03:54.052302",
            "name": "California",
        }
        state = State(**kwargs)
        self.assertEqual(state.id, "f7f99")
        self.assertEqual(
            state.created_at,
            datetime.strptime("2017-09-28T21:03:54.052298", time_format),
        )
        self.assertEqual(
            state.updated_at,
            datetime.strptime("2017-09-28T21:03:54.052302", time_format),
        )
        self.assertEqual(state.name, "California")

    def test_extra_kwargs(self):
        time_format = "%Y-%m-%dT%H:%M:%S.%f"
        kwargs = {
            "id": "f7f99",
            "created_at": "2017-09-28T21:03:54.052298",
            "updated_at": "2017-09-28T21:03:54.052302",
            "name": "California",
            "text": "Holberton School is awesome!",
        }
        state = State(**kwargs)
        self.assertEqual(state.id, "f7f99")
        self.assertEqual(
            state.created_at,
            datetime.strptime("2017-09-28T21:03:54.052298", time_format),
        )
        self.assertEqual(
            state.updated_at,
            datetime.strptime("2017-09-28T21:03:54.052302", time_format),
        )
        self.assertEqual(state.name, "California")
        self.assertNotIn("text", state.__dict__)


class TestState_save(unittest.TestCase):
    """Unittests for testing save() method of the State class."""

    def setUp(self):
        try:
            os.remove("file.json")
        except:
            pass
        State._State__objects = {}

    def test_save_updates_updated_at(self):
        state = State()
        old_updated_at = state.updated_at
        sleep(0.1)
        state.save()
        self.assertLess(old_updated_at, state.updated_at)

    def test_save_updates_file(self):
        state = State()
        state.save()
        with open("file.json", "r") as f:
            self.assertIn(state.id, f.read())

    def test_save_with_args(self):
        state = State()
        with self.assertRaises(TypeError):
            state.save(None)

    def test_save_with_kwargs(self):
        state = State()
        with self.assertRaises(TypeError):
            state.save(state_id="CA")

    def test_save_no_args(self):
        state = State()
        state.save()
        key = "{}.{}".format(type(state).__name__, state.id)
        self.assertIn(key, State._State__objects.keys())

    def test_save_one_arg(self):
        state = State()
        with self.assertRaises(TypeError):
            state.save(1)

    def test_save_multiple_args(self):
        state = State()
        with self.assertRaises(TypeError):
            state.save(1, 2)

    def test_save_no_private_attrs(self):
        state = State()
        state.save()
        with open("file.json", "r") as f:
            obj = eval(f.read())
            self.assertNotIn("__class__", obj.values())
            self.assertNotIn("updated_at", obj.values())
            self.assertNotIn("created_at", obj.values())

    def test_save_updated_at_format(self):
        state = State()
        state.save()
        with open("file.json", "r") as f:
            obj = eval(f.read())
            for value in obj.values():
                if type(value) == dict:
                    self.assertEqual("%Y-%m-%dT%H:%M:%S.%f", value["updated_at"][19:-3])

    def test_save_created_at_format(self):
        state = State()
        state.save()
        with open("file.json", "r") as f:
            obj = eval(f.read())
            for value in obj.values():
                if type(value) == dict:
                    self.assertEqual("%Y-%m-%dT%H:%M:%S.%f", value["created_at"][19:-3])


class TestState_to_dict(unittest.TestCase):
    """Unittests for testing to_dict() method of the State class."""

    def test_to_dict_type(self):
        self.assertEqual(dict, type(State().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        self.assertIn("id", State().to_dict())
        self.assertIn("created_at", State().to_dict())
        self.assertIn("updated_at", State().to_dict())
        self.assertIn("__class__", State().to_dict())

    def test_to_dict_contains_added_attrs(self):
        state = State()
        state.name = "California"
        state.number = 1
        d = state.to_dict()
        self.assertIn("name", d)
        self.assertIn("number", d)

    def test_to_dict_datetime_format(self):
        state = State()
        state_dict = state.to_dict()
        self.assertEqual("%Y-%m-%dT%H:%M:%S.%f", state_dict["created_at"][19:-3])
        self.assertEqual("%Y-%m-%dT%H:%M:%S.%f", state_dict["updated_at"][19:-3])

    def test_to_dict_classname(self):
        state = State()
        state_dict = state.to_dict()
        self.assertEqual("State", state_dict["__class__"])

    def test_to_dict_output(self):
        state = State()
        state.id = "f7f99"
        state.created_at = datetime(2017, 9, 28, 21, 3, 54, 52298)
        state.updated_at = datetime(2017, 9, 28, 21, 3, 54, 52302)
        state.name = "California"
        state_dict = state.to_dict()
        expected = {
            "id": "f7f99",
            "__class__": "State",
            "created_at": "2017-09-28T21:03:54.052298",
            "updated_at": "2017-09-28T21:03:54.052302",
            "name": "California",
        }
        self.assertDictEqual(expected, state_dict)

    def test_to_dict_input(self):
        state = State()
        state_dict = state.to_dict()
        self.assertEqual(state_dict["id"], state.id)
        self.assertEqual(state_dict["created_at"], state.created_at.isoformat())
        self.assertEqual(state_dict["updated_at"], state.updated_at.isoformat())


class TestState_str(unittest.TestCase):
    """Unittests for testing __str__ method of the State class."""

    def test_str(self):
        state = State()
        string = "[{}] ({}) {}".format(type(state).__name__, state.id, state.__dict__)
        self.assertEqual(string, str(state))

    def test_str_format(self):
        state = State()
        string = str(state)
        self.assertEqual("[State]", string[0:7])
        self.assertEqual("({})".format(state.id), string[8:33])
        self.assertEqual("{", string[34])
        self.assertEqual("}", string[-1])

    def test_str_output(self):
        state = State()
        state.id = "f7f99"
        state.created_at = datetime(2017, 9, 28, 21, 3, 54, 52298)
        state.updated_at = datetime(2017, 9, 28, 21, 3, 54, 52302)
        state.name = "California"
        string = "[{}] ({}) {}".format(type(state).__name__, state.id, state.__dict__)
        self.assertEqual(string, str(state))

    def test_str_input(self):
        state = State()
        string = str(state)
        self.assertEqual(string, "[State] ({}) {}".format(state.id, state.__dict__))

    def test_str_classname(self):
        state = State()
        string = str(state)
        self.assertEqual(string[1:6], "State")


if __name__ == "__main__":
    unittest.main()
