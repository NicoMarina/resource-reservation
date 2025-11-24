from django.db import models
from .resource import Resource


class Equipment(Resource):
    """
    Model representing an equipment resource.
    Inherits from the base Resource model.
    - Hour-based or day-based reservations
    """

    def get_type(self):
        return "equipment"

    def get_attributes(self):
        return {}
