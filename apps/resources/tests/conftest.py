from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from apps.resources.models import MeetingRoom, Vehicle, Equipment
import warnings

warnings.simplefilter("ignore", RuntimeWarning)


class ResourceTestSetup(TestCase):
    """Sets up test data for Resource-related tests."""

    @classmethod
    def setUpTestData(cls):
        # Meeting Room
        cls.meeting_room = MeetingRoom.objects.create(
            name="Conference Room A",
            description="A large conference room",
            capacity=20,
            image_url="http://example.com/meeting.png",
        )

        # Vehicle
        cls.vehicle = Vehicle.objects.create(
            name="Company Car",
            description="A car for business trips",
            image_url="http://example.com/car.png",
        )

        # Equipment
        cls.equipment = Equipment.objects.create(
            name="Projector",
            description="HD Projector",
            image_url="http://example.com/projector.png",
        )
