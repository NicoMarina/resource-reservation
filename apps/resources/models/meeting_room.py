from django.db import models
from .resource import Resource


class MeetingRoom(Resource):
    """
    Model representing a meeting room resource.
    Inherits from the base Resource model.
    - Hour-based reservations
    - Maximum capacity
    """

    capacity = models.IntegerField()
