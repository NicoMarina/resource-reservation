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
