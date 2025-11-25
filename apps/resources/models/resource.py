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

    def get_max_capacity(self):
        """Return the maximum capacity of the resource."""
        raise NotImplementedError

    def check_availability(self, date, start_time=None, end_time=None):
        """Check if the resource is available for the given date and time."""
        raise NotImplementedError

