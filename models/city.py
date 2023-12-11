#!/usr/bin/python3

"""model state class from the main class BaseModel"""

from models.base_model import BaseModel


class City(BaseModel):

    """child class of BaseModel with 2 attributes of the city"""

    state_id = ""
    name = ""
