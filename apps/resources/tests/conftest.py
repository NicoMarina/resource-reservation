from django.test import TestCase
from apps.resources.models import MeetingRoom, Vehicle, Equipment
from apps.resources.models import FlexiblePolicy, ModeratePolicy, BlockedPolicy
import warnings

warnings.simplefilter("ignore", RuntimeWarning)


class ResourceTestSetup(TestCase):
    """Sets up test data for Resource-related tests."""

    @classmethod
    def setUpTestData(cls):
        cls.flexible_policy = FlexiblePolicy.objects.create(name="Flexible")
        cls.moderate_policy = ModeratePolicy.objects.create(name="Moderate")
        cls.blocked_policy = BlockedPolicy.objects.create(name="Blocked")

        # Meeting Room
        cls.meeting_room = MeetingRoom.objects.create(
            name="Conference Room A",
            description="A large conference room",
            capacity=20,
            image_url="http://example.com/meeting.png",
            cancellation_policy=cls.flexible_policy,
        )

        # Vehicle
        cls.vehicle = Vehicle.objects.create(
            name="Company Car",
            description="A car for business trips",
            image_url="http://example.com/car.png",
            cancellation_policy=cls.moderate_policy,
        )

        # Equipment
        cls.equipment = Equipment.objects.create(
            name="Projector",
            description="HD Projector",
            image_url="http://example.com/projector.png",
            cancellation_policy=cls.blocked_policy,
        )
