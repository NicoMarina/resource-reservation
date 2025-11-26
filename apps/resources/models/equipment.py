from django.db import models
from .resource import Resource
from apps.reservations.models.reservation import Reservation
from apps.reservations.services import (
    calculate_free_hours,
    serialize_blocking_reservations,
    get_reservations_info,
)
from datetime import datetime, timedelta, time


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

    def is_hourly(self):
        return True

    def is_daily(self):
        return True

    def check_availability(
        self, date, start_time=None, end_time=None, used_capacity=None
    ):
        start_time = start_time or time(8, 0)
        end_time = end_time or time(20, 0)

        reservations = Reservation.objects.filter(resource=self, date=date)
        free_hours = calculate_free_hours(reservations, start_time, end_time)
        reservations_info = get_reservations_info(
            reservations, self, start_time, end_time
        )

        available = len(reservations_info["blocking_reservations"]) == 0

        return {
            "resource_id": self.id,
            "available": available,
            "free_hours": free_hours,
            **reservations_info,
            "reason": None if available else "Time slot already booked",
        }
