from django.db import models
from polymorphic.models import PolymorphicModel


class Resource(PolymorphicModel):
    """
    Base resource model with polymorphic behavior.
    All resource types inherit from this class.
    """

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)

    def get_type(self):
        """Return the type of the resource as a string."""
        raise NotImplementedError

    def get_attributes(self):
        """Return a dictionary of resource-specific attributes."""
        raise NotImplementedError

    def is_hourly(self):
        """Return True if the resource is booked hourly, False otherwise."""
        raise NotImplementedError

    def is_daily(self):
        """Return True if the resource is booked daily, False otherwise."""
        raise NotImplementedError

    def allow_shared_capacity(self):
        """Return True if the resource allows shared capacity bookings."""
        return False

    def check_availability(
        self, date, start_time=None, end_time=None, used_capacity=None
    ):
        """Check if the resource is available for the given date and time."""
        raise NotImplementedError

    def create_reservation(
        self, date, start_time=None, end_time=None, used_capacity=None
    ):
        from apps.reservations.models import Reservation

        return Reservation.objects.create(
            resource=self,
            date=date,
            start_time=start_time if self.is_hourly() else None,
            end_time=end_time if self.is_hourly() else None,
            used_capacity=used_capacity if self.allow_shared_capacity() else None,
        )
