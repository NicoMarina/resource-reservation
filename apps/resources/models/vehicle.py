from django.db import models
from .resource import Resource


class Vehicle(Resource):
    """
    Model representing a vehicle resource.
    Inherits from the base Resource model.
    - Day-based reservations
    """

    def get_type(self):
        return "vehicle"

    def get_attributes(self):
        return {}
