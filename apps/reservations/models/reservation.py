from django.db import models
from apps.resources.models import Resource
from django.contrib.auth.models import User
from django.conf import settings


class Reservation(models.Model):
    """Model representing a reservation of a resource."""

    STATUS_CHOICES = [
        ("pending", "Pending Approval"),
        ("approved", "Approved"),
    ]

    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    full_day = models.BooleanField(default=False)
    used_capacity = models.PositiveIntegerField(null=True, blank=True)
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_reservations",
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_reservations",
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    class Meta:
        ordering = ("date", "start_time")

    def is_pending(self):
        return self.status == "pending"

    def is_approved(self):
        return self.status == "approved"
