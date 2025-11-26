from django.db import models
from django.utils import timezone
from polymorphic.models import PolymorphicModel
from rest_framework.exceptions import ValidationError
from datetime import datetime
from apps.common.utils import normalize_reservation_inputs


class CancellationPolicy(PolymorphicModel):
    name = models.CharField(max_length=50)

    def can_cancel(self, reservation, user):
        """
        Polymorphic method that defines whether a reservation can be canceled.
        Must be implemented by each subclass.
        """
        raise NotImplementedError


class FlexiblePolicy(CancellationPolicy):
    def can_cancel(self, reservation, user):
        date, start_time, _ = normalize_reservation_inputs(
            reservation.date.isoformat(),
            start_time=reservation.start_time,
            end_time=reservation.end_time,
        )
        start_dt = timezone.make_aware(datetime.combine(date, start_time))
        # Cancellation up to 1 hour before
        deadline = start_dt - timezone.timedelta(hours=1)
        return timezone.now() <= deadline


class ModeratePolicy(CancellationPolicy):
    def can_cancel(self, reservation, user):
        date, start_time, _ = normalize_reservation_inputs(
            reservation.date.isoformat(),
            start_time=reservation.start_time,
            end_time=reservation.end_time,
        )
        start_dt = timezone.make_aware(datetime.combine(date, start_time))
        # Cancellation up to 24 hours in advance
        deadline = start_dt - timezone.timedelta(hours=24)
        return timezone.now() <= deadline


class BlockedPolicy(CancellationPolicy):
    def can_cancel(self, reservation, user):
        # Can't cancel
        return False
