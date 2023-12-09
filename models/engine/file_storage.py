#!/usr/bin/python3
"""This module creates a FileStorage class"""
import datetime
import json
import os


class FileStorage:
    """Class for serializing and deserializing objects to and from JSON."""

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Returns the dictionary __objects."""
        return FileStorage.__objects

    def new(self, obj):
        """Sets in __objects the obj with key <obj class name>.id."""
        key = "{}.{}".format(type(obj).__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """Serializes __objects to the JSON file (path: __file_path)."""
        new_dict = {}
        for key, value in FileStorage.__objects.items():
            new_dict[key] = value.to_dict()
        with open(FileStorage.__file_path, "w") as f:
            json.dump(new_dict, f)

    def reload(self):
        """Deserializes the JSON file to __objects (only if the JSON file
        (__file_path) exists; otherwise, do nothing. If the file doesn’t
        exist, no exception should be raised)."""
        try:
            with open(FileStorage.__file_path, "r") as f:
                new_dict = json.load(f)
            for key, value in new_dict.items():
                FileStorage.__objects[key] = eval(value["__class__"])(**value)
        except:
            pass

    def delete(self, obj=None):
        """Deletes obj from __objects if it’s inside."""
        if obj is not None:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            if key in FileStorage.__objects:
                del FileStorage.__objects[key]

    def close(self):
        """Deserializes the JSON file to objects."""
        self.reload()

    def classes(self):
        """Returns a dictionary of valid classes."""
        from models.base_model import BaseModel
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review

        return {
            "BaseModel": BaseModel,
            "User": User,
            "State": State,
            "City": City,
            "Amenity": Amenity,
            "Place": Place,
            "Review": Review,
        }

    def all(self):
        """Returns the dictionary __objects."""
        return FileStorage.__objects

    def new(self, obj):
        """Sets in __objects the obj with key <obj class name>.id."""
        key = "{}.{}".format(type(obj).__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """Serializes __objects to the JSON file (path: __file_path)."""
        new_dict = {}
        for key, value in FileStorage.__objects.items():
            new_dict[key] = value.to_dict()
        with open(FileStorage.__file_path, "w") as f:
            json.dump(new_dict, f)

