from django.db import models
from .resource import Resource
from apps.reservations.models.reservation import Reservation
from apps.reservations.services import (
    get_reservations_info,
)


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

    def is_hourly(self):
        return False

    def is_daily(self):
        return True

    def check_availability(
        self, date, start_time=None, end_time=None, used_capacity=None
    ):
        """
        Checks if the vehicle is available on a given day.
        Ignores start_time/end_time since vehicle is daily.
        """
        reservations = Reservation.objects.filter(resource=self, date=date)
        reservations_info = get_reservations_info(reservations, self)
        available = len(reservations_info["blocking_reservations"]) == 0

        return {
            "resource_id": self.id,
            "available": available,
            **reservations_info,
            "reason": None if available else "Vehicle already booked",
        }
