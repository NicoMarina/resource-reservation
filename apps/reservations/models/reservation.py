from django.db import models
from apps.resources.models import Resource


class Reservation(models.Model):
    """Model representing a reservation of a resource."""

    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    full_day = models.BooleanField(default=False)
    used_capacity = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        ordering = ("date", "start_time")
