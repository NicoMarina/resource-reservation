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

    def get_type(self):
        return "meeting_room"

    def get_attributes(self):
        return {"capacity": self.capacity}
