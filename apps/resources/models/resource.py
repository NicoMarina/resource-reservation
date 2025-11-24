from django.db import models


class Resource(models.Model):
    """
    Base Model.
    Common fields for all resources.
    """

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True
