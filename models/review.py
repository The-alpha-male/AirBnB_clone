#!/usr/bin/python3

"""model class review
"""

from models.base_model import BaseModel


class Review(BaseModel):

    """subclass of BaseModel and represents a review
    with attributes for place_id,user_id, and text
    """

    place_id = ""
    user_id = ""
    text = ""
