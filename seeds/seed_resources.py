# seed/seed_resources.py
import os
import django

# Configura Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "resource_reservation.settings")
django.setup()

from apps.resources.models import MeetingRoom, Vehicle, Equipment


def run():
    # Limpiar datos existentes
    MeetingRoom.objects.all().delete()
    Vehicle.objects.all().delete()
    Equipment.objects.all().delete()

    # Crear meeting rooms
    MeetingRoom.objects.create(
        name="Conference Room A",
        description="A large conference room",
        capacity=20,
        image_url="http://example.com/meeting.png",
    )
    MeetingRoom.objects.create(
        name="Conference Room B",
        description="Medium size room",
        capacity=10,
        image_url="http://example.com/meeting2.png",
    )

    # Crear vehicles
    Vehicle.objects.create(
        name="Company Car",
        description="Car for business trips",
        image_url="http://example.com/car.png",
    )
    Vehicle.objects.create(
        name="Van",
        description="Transport van",
        image_url="http://example.com/van.png",
    )

    # Crear equipments
    Equipment.objects.create(
        name="Projector",
        description="HD Projector",
        image_url="http://example.com/projector.png",
    )
    Equipment.objects.create(
        name="Whiteboard",
        description="Magnetic whiteboard",
        image_url="http://example.com/whiteboard.png",
    )

    print("Resources seeded successfully!")


if __name__ == "__main__":
    run()
