from django.db import models
from .resource import Resource
from apps.reservations.models.reservation import Reservation
from apps.reservations.services import (
    overlaps,
    calculate_free_hours,
    sum_used_capacity,
    get_reservations_info,
)
from datetime import time


class MeetingRoom(Resource):
    """
    Model representing a meeting room resource.
    Inherits from the base Resource model.
    - Hour-based reservations
    - Maximum capacity
    - Allows shared capacity
    """

    capacity = models.IntegerField()

    def get_type(self):
        return "meeting_room"

    def get_attributes(self):
        return {"capacity": self.capacity}

    def is_hourly(self):
        return True

    def allow_shared_capacity(self):
        return True

    def check_availability(
        self, date, start_time=None, end_time=None, used_capacity=None
    ):
        start_time = start_time or time(8, 0)
        end_time = end_time or time(20, 0)
        used_capacity = int(used_capacity or 1)

        office_start, office_end = time(8, 0), time(20, 0)
        if start_time < office_start or end_time > office_end:
            return {
                "resource_id": self.id,
                "available": False,
                "reason": "Outside office hours",
            }

        reservations = Reservation.objects.filter(resource=self, date=date)

        used_approved = sum_used_capacity(reservations, start_time, end_time)
        remaining_capacity = self.capacity - used_approved
        available = remaining_capacity >= used_capacity

        free_hours = calculate_free_hours(reservations, office_start, office_end)

        reservations_info = get_reservations_info(
            reservations, self, start_time, end_time
        )

        return {
            "resource_id": self.id,
            "available": available,
            "capacity_total": self.capacity,
            "capacity_used": used_approved,
            "capacity_remaining": max(0, remaining_capacity),
            "free_hours": free_hours,
            **reservations_info,
            "reason": None if available else "Capacity exceeded",
        }
