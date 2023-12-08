#!/usr/bin/python3

"""model user class"""

from models.base_model import BaseModel


"""The User class is a subclass
of BaseModel and represents a
user with email, password, first name,
and last name attributes."""


class User(BaseModel):

    email = ""
    password = ""
    first_name = ""
    last_name = ""
