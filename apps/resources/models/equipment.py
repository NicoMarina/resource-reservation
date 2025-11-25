from django.db import models
from .resource import Resource
from apps.reservations.models.reservation import Reservation
from apps.reservations.services.availability_utils import overlaps, calculate_free_hours
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

        # Filtrar reservas del día
        reservations = Reservation.objects.filter(resource=self, date=date)

        # Franjas libres (solo para visualización)
        free_hours = calculate_free_hours(reservations, start_time, end_time)
        for slot in free_hours:
            slot["start"] = slot["start"].strftime("%H:%M")
            slot["end"] = slot["end"].strftime("%H:%M")

        # Comprobar si el slot solicitado está libre
        requested_overlap = [
            r
            for r in reservations
            if overlaps(r.start_time, r.end_time, start_time, end_time)
        ]
        available = len(requested_overlap) == 0

        return {
            "resource_id": self.id,
            "available": available,
            "free_hours": free_hours,
            "blocking_reservations": [
                {
                    "id": r.id,
                    "start_time": r.start_time.strftime("%H:%M"),
                    "end_time": r.end_time.strftime("%H:%M"),
                }
                for r in requested_overlap
            ],
            "reason": None if available else "Time slot already booked",
        }
