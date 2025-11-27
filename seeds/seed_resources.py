import os
import django

# Confihure Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "resource_reservation.settings")
django.setup()

from apps.resources.models import MeetingRoom, Vehicle, Equipment
from apps.resources.models.cancellation_policy import (
    FlexiblePolicy,
    ModeratePolicy,
    BlockedPolicy,
)


def run():
    # Clean up existing data
    MeetingRoom.objects.all().delete()
    Vehicle.objects.all().delete()
    Equipment.objects.all().delete()

    flexible, _ = FlexiblePolicy.objects.get_or_create(name="Flexible")
    moderate, _ = ModeratePolicy.objects.get_or_create(name="Moderate")
    blocked, _ = BlockedPolicy.objects.get_or_create(name="Blocked")

    # Create meeting rooms
    MeetingRoom.objects.create(
        name="Conference Room A",
        description="A large conference room",
        capacity=20,
        image_url="http://example.com/meeting.png",
        cancellation_policy=flexible,
    )
    MeetingRoom.objects.create(
        name="Conference Room B",
        description="Medium size room",
        capacity=10,
        image_url="http://example.com/meeting2.png",
        cancellation_policy=moderate,
    )

    # Create vehicles
    Vehicle.objects.create(
        name="Company Car",
        description="Car for business trips",
        image_url="http://example.com/car.png",
        cancellation_policy=blocked,
    )
    Vehicle.objects.create(
        name="Van",
        description="Transport van",
        image_url="http://example.com/van.png",
        cancellation_policy=blocked,
    )

    # Create equipments
    Equipment.objects.create(
        name="Projector",
        description="HD Projector",
        image_url="http://example.com/projector.png",
        cancellation_policy=moderate,
    )
    Equipment.objects.create(
        name="Whiteboard",
        description="Magnetic whiteboard",
        image_url="http://example.com/whiteboard.png",
        cancellation_policy=flexible,
    )

    print("Resources seeded successfully!")


if __name__ == "__main__":
    run()
