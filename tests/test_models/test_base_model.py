#!/usr/bin/python3
"""Unittest for base_model.py"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.base_model import BaseModel


class TestBaseModel_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the BaseModel class."""

    def test_no_args_instantiates(self):
        self.assertEqual(BaseModel, type(BaseModel()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(BaseModel(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(BaseModel().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(BaseModel().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(BaseModel().updated_at))

    def test_args_unused(self):
        self.assertNotIn("__init__", BaseModel.__dict__)

    def test_instantiation_with_no_kwargs(self):
        bm = BaseModel()
        self.assertEqual(bm.id, bm.id)
        self.assertEqual(bm.created_at, bm.created_at)
        self.assertEqual(bm.updated_at, bm.updated_at)

    def test_instantiation_with_all_kwargs(self):
        time_format = "%Y-%m-%dT%H:%M:%S.%f"
        kwargs = {
            "id": "f7f99",
            "created_at": "2017-09-28T21:03:54.052298",
            "updated_at": "2017-09-28T21:03:54.052302",
        }
        bm = BaseModel(**kwargs)
        self.assertEqual(bm.id, "f7f99")
        self.assertEqual(
            bm.created_at,
            datetime.strptime("2017-09-28T21:03:54.052298", time_format),
        )
        self.assertEqual(
            bm.updated_at,
            datetime.strptime("2017-09-28T21:03:54.052302", time_format),
        )

    def test_instantiation_with_some_kwargs(self):
        time_format = "%Y-%m-%dT%H:%M:%S.%f"
        kwargs = {
            "created_at": "2017-09-28T21:03:54.052298",
            "updated_at": "2017-09-28T21:03:54.052302",
        }
        bm = BaseModel(**kwargs)
        self.assertNotEqual(bm.id, "")
        self.assertEqual(
            bm.created_at,
            datetime.strptime("2017-09-28T21:03:54.052298", time_format),
        )
        self.assertEqual(
            bm.updated_at,
            datetime.strptime("2017-09-28T21:03:54.052302", time_format),
        )

    def test_id_is_None(self):
        bm = BaseModel()
        self.assertIsNone(bm.id)

    def test_created_at_is_None(self):
        bm = BaseModel()
        self.assertIsNone(bm.created_at)

    def test_updated_at_is_None(self):
        bm = BaseModel()
        self.assertIsNone(bm.updated_at)

    def test_two_models_unique_ids(self):
        bm1 = BaseModel()
        bm2 = BaseModel()
        self.assertNotEqual(bm1.id, bm2.id)

    def test_two_models_different_created_at(self):
        bm1 = BaseModel()
        sleep(0.1)
        bm2 = BaseModel()
        self.assertLess(bm1.created_at, bm2.created_at)

    def test_two_models_different_updated_at(self):
        bm1 = BaseModel()
        sleep(0.1)
        bm2 = BaseModel()
        self.assertLess(bm1.updated_at, bm2.updated_at)

    def test_str_method(self):
        bm = BaseModel()
        self.assertEqual("[BaseModel] ({}) {}".format(bm.id, bm.__dict__), str(bm))

    def test_save_updates_updated_at(self):
        bm = BaseModel()
        old_updated_at = bm.updated_at
        sleep(0.1)
        bm.save()
        self.assertLess(old_updated_at, bm.updated_at)

    def test_save_updates_file(self):
        bm = BaseModel()
        bm.save()
        with open("file.json", "r") as f:
            self.assertIn(bm.id, f.read())

    def test_save_with_args(self):
        bm = BaseModel()
        with self.assertRaises(TypeError):
            bm.save(None)

    def test_save_with_kwargs(self):
        bm = BaseModel()
        with self.assertRaises(TypeError):
            bm.save(state_id="CA")

    def test_save_no_args(self):
        bm = BaseModel()
        bm.save()
        self.assertNotEqual(bm.created_at, bm.updated_at)

    def test_save_one_arg(self):
        bm = BaseModel()
        with self.assertRaises(TypeError):
            bm.save(1)

    def test_save_multiple_args(self):
        bm = BaseModel()
        with self.assertRaises(TypeError):
            bm.save(1, 2)

    def test_save_no_private_attrs(self):
        bm = BaseModel()
        bm.save()
        with open("file.json", "r") as f:
            obj = eval(f.read())
            self.assertNotIn("__class__", obj.values())
            self.assertNotIn("updated_at", obj.values())
            self.assertNotIn("created_at", obj.values())

    def test_save_updated_at_format(self):
        bm = BaseModel()
        bm.save()
        with open("file.json", "r") as f:
            obj = eval(f.read())
            for value in obj.values():
                if type(value) == dict:
                    self.assertEqual(
                        value["updated_at"],
                        bm.updated_at.isoformat(),
                    )

    def test_save_created_at_format(self):
        bm = BaseModel()
        bm.save()
        with open("file.json", "r") as f:
            obj = eval(f.read())
            for value in obj.values():
                if type(value) == dict:
                    self.assertEqual(
                        value["created_at"],
                        bm.created_at.isoformat(),
                    )

    def test_to_dict(self):
        bm = BaseModel()
        bm_dict = bm.to_dict()
        self.assertEqual(dict, type(bm_dict))
        self.assertIn("__class__", bm_dict)
        self.assertEqual("BaseModel", bm_dict["__class__"])
        self.assertEqual(str, type(bm_dict["id"]))
        self.assertEqual(bm.id, bm_dict["id"])
        self.assertEqual(datetime, type(bm_dict["created_at"]))
        self.assertEqual(bm.created_at.isoformat(), bm_dict["created_at"])
        self.assertEqual(datetime, type(bm_dict["updated_at"]))
        self.assertEqual(bm.updated_at.isoformat(), bm_dict["updated_at"])

    def test_to_dict_no_args(self):
        with self.assertRaises(TypeError):
            BaseModel.to_dict()

    def test_to_dict_extra_args(self):
        with self.assertRaises(TypeError):
            BaseModel.to_dict(None)

    def test_to_dict_one_arg(self):
        with self.assertRaises(TypeError):
            BaseModel.to_dict("Betty")

    def test_to_dict_two_args(self):
        with self.assertRaises(TypeError):
            BaseModel.to_dict("Betty", "Holberton")

    def test_to_dict_update(self):
        from models import storage
        from models.base_model import BaseModel
        from os import path
        import json
        import os

        bm1 = BaseModel()
        bm1_dict = bm1.to_dict()
        bm1.save()
        bm1_id = "BaseModel." + bm1.id
        storage.reload()
        self.assertEqual(storage.all()[bm1_id].to_dict(), bm1.to_dict())
        bm1.save()
        storage.reload()
        self.assertEqual(storage.all()[bm1_id].to_dict(), bm1.to_dict())
        with open("file.json", "r") as f:
            obj = eval(f.read())
            self.assertEqual(obj[bm1_id], bm1.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        bm = BaseModel()
        bm_dict = bm.to_dict()
        self.assertEqual(str, type(bm_dict["id"]))
        self.assertEqual(str, type(bm_dict["created_at"]))
        self.assertEqual(str, type(bm_dict["updated_at"]))

    def test_to_dict_with_arg(self):
        with self.assertRaises(TypeError):
            BaseModel.to_dict(None)

    def test_to_dict_with_kwargs(self):
        with self.assertRaises(TypeError):
            BaseModel.to_dict(state_id="CA")

    def test_to_dict_with_one_arg(self):
        with self.assertRaises(TypeError):
            BaseModel.to_dict(1)

    def test_to_dict_with_multiple_args(self):
        with self.assertRaises(TypeError):
            BaseModel.to_dict(1, 2)

    def test_to_dict_with_extra_self(self):
        with self.assertRaises(TypeError):
            BaseModel.to_dict(self, 98)

    def test_to_dict_with_extra_cls(self):
        with self.assertRaises(TypeError):
            BaseModel.to_dict(BaseModel, 98)

    def test_to_dict_with_extra_cls_and_dict(self):
        with self.assertRaises(TypeError):
            BaseModel.to_dict(BaseModel, {"id": 98})

    def test_to_dict_with_extra_cls_and_dict_and_extra(self):
        with self.assertRaises(TypeError):
            BaseModel.to_dict(BaseModel, {"id": 98}, 98)

    def test_to_dict_with_extra_dict(self):
        with self.assertRaises(TypeError):
            BaseModel.to_dict({"id": 98})

    def test_to_dict_with_extra_dict_and_extra(self):
        with self.assertRaises(TypeError):
            BaseModel.to_dict({"id": 98}, 98)

    def test_to_dict_with_extra_dict_and_extra_self(self):
        with self.assertRaises(TypeError):
            BaseModel.to_dict({"id": 98}, self)

    def test_to_dict_with_extra_dict_and_extra_cls(self):
        with self.assertRaises(TypeError):
            BaseModel.to_dict({"id": 98}, BaseModel)

    def test_to_dict_with_extra_dict_and_extra_cls_and_extra(self):
        with self.assertRaises(TypeError):
            BaseModel.to_dict({"id": 98}, BaseModel, 98)

    def test_to_dict_with_extra_dict_and_extra_cls_and_extra_self(self):
        with self.assertRaises(TypeError):
            BaseModel.to_dict({"id": 98}, BaseModel, self)

    def test_to_dict_with_extra_dict_and_extra_cls_and_extra_dict(self):
        with self.assertRaises(TypeError):
            BaseModel.to_dict({"id": 98}, BaseModel, {"id": 98})

    def test_to_dict_with_extra_dict_and_extra_cls_and_extra_dict_and_extra(self):
        with self.assertRaises(TypeError):
            BaseModel.to_dict({"id": 98}, BaseModel, {"id": 98}, 98)

    def test_to_dict_with_extra_dict_and_extra_cls_and_extra_dict_and_extra_self(self):
        with self.assertRaises(TypeError):
            BaseModel.to_dict({"id": 98}, BaseModel, {"id": 98}, self)


class TestBaseModel_save(unittest.TestCase):
    """Unittests for testing save method of the BaseModel class."""

    def setUp(self):
        try:
            os.remove("file.json")
        except:
            pass

    def tearDown(self):
        try:
            os.remove("file.json")
        except:
            pass

    def test_save(self):
        bm = BaseModel()
        bm.save()
        with open("file.json", "r") as f:
            self.assertIn(bm.id, f.read())

    def test_save_no_args(self):
        bm = BaseModel()
        with self.assertRaises(TypeError):
            bm.save(None)

    def test_save_with_args(self):
        bm = BaseModel()
        with self.assertRaises(TypeError):
            bm.save(1)

    def test_save_with_kwargs(self):
        bm = BaseModel()
        with self.assertRaises(TypeError):
            bm.save(state_id="CA")

    def test_save_one_arg(self):
        bm = BaseModel()
        with self.assertRaises(TypeError):
            bm.save(1)

    def test_save_multiple_args(self):
        bm = BaseModel()
        with self.assertRaises(TypeError):
            bm.save(1, 2)

    def test_save_no_private_attrs(self):
        bm = BaseModel()
        bm.save()
        with open("file.json", "r") as f:
            obj = eval(f.read())
            self.assertNotIn("__class__", obj.values())
            self.assertNotIn("updated_at", obj.values())
            self.assertNotIn("created_at", obj.values())

    def test_save_updated_at_format(self):
        bm = BaseModel()
        bm.save()
        with open("file.json", "r") as f:
            obj = eval(f.read())
            for value in obj.values():
                if type(value) == dict:
                    self.assertEqual(
                        value["updated_at"],
                        bm.updated_at.isoformat(),
                    )

    def test_save_created_at_format(self):
        bm = BaseModel()
        bm.save()
        with open("file.json", "r") as f:
            obj = eval(f.read())
            for value in obj.values():
                if type(value) == dict:
                    self.assertEqual(
                        value["created_at"],
                        bm.created_at.isoformat(),
                    )

    def test_save_updated_at(self):
        bm = BaseModel()
        old_updated_at = bm.updated_at
        sleep(0.1)
        bm.save()
        self.assertLess(old_updated_at, bm.updated_at)

    def test_save_file(self):
        bm = BaseModel()
        bm.save()
        with open("file.json", "r") as f:
            self.assertIn(bm.id, f.read())


if __name__ == "__main__":
    unittest.main()
