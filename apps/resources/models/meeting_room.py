from django.db import models
from .resource import Resource
from apps.reservations.models.reservation import Reservation
from apps.reservations.services.availability_utils import overlaps, calculate_free_hours
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

    def check_availability(self, date, start_time=None, end_time=None):
        start_time = start_time or time(8, 0)
        end_time = end_time or time(20, 0)

        # Filtrar reservas del día
        reservations = Reservation.objects.filter(resource=self, date=date)

        # Franjas libres
        free_hours = calculate_free_hours(reservations, start_time, end_time)

        # Capacidad en cada franja
        for slot in free_hours:
            overlapping = [
                r
                for r in reservations
                if overlaps(r.start_time, r.end_time, slot["start"], slot["end"])
            ]
            slot["available_capacity"] = max(
                0,
                self.capacity
                - sum(getattr(r, "used_capacity", 1) for r in overlapping),
            )
            slot["start"] = slot["start"].strftime("%H:%M")
            slot["end"] = slot["end"].strftime("%H:%M")

        # Capacidad en slot solicitado
        requested_overlap = [
            r
            for r in reservations
            if overlaps(r.start_time, r.end_time, start_time, end_time)
        ]
        used_capacity = sum(getattr(r, "used_capacity", 1) for r in requested_overlap)
        remaining_capacity = self.capacity - used_capacity

        return {
            "resource_id": self.id,
            "available": remaining_capacity > 0,
            "capacity_total": self.capacity,
            "capacity_used": used_capacity,
            "capacity_remaining": remaining_capacity,
            "free_hours": free_hours,
            "blocking_reservations": [
                {
                    "id": r.id,
                    "start_time": r.start_time.strftime("%H:%M"),
                    "end_time": r.end_time.strftime("%H:%M"),
                    "used_capacity": r.used_capacity,
                }
                for r in requested_overlap
            ],
            "reason": None if remaining_capacity > 0 else "Capacity exceeded",
        }
