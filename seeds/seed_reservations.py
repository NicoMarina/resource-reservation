import os
import django
from datetime import datetime, time, timezone

# Configure Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "resource_reservation.settings")
django.setup()

from apps.resources.models import MeetingRoom, Vehicle, Equipment
from apps.reservations.models import Reservation


def run():
    # Clean up existing data
    Reservation.objects.all().delete()

    # Get resources
    rooms = MeetingRoom.objects.all()
    vehicles = Vehicle.objects.all()
    equipments = Equipment.objects.all()

    room_a, room_b = rooms[0], rooms[1]
    vehicle_a, vehicle_b = vehicles[0], vehicles[1]
    projector, whiteboard = equipments[0], equipments[1]

    # Create meeting rooms reservations
    # Room A
    Reservation.objects.create(
        resource=room_a,
        date=datetime(2025, 11, 23, tzinfo=timezone.utc).date(),
        start_time=time(9, 0),
        end_time=time(11, 0),
        used_capacity=10,
    )
    Reservation.objects.create(
        resource=room_a,
        date=datetime(2025, 11, 23, tzinfo=timezone.utc).date(),
        start_time=time(14, 0),
        end_time=time(16, 0),
        used_capacity=20,
    )
    Reservation.objects.create(
        resource=room_a,
        date=datetime(2025, 11, 23, tzinfo=timezone.utc).date(),
        start_time=time(15, 0),
        end_time=time(16, 0),
        used_capacity=10,
    )
    Reservation.objects.create(
        resource=room_a,
        date=datetime(2025, 11, 24, tzinfo=timezone.utc).date(),
        start_time=time(9, 0),
        end_time=time(10, 0),
        used_capacity=1,
    )
    Reservation.objects.create(
        resource=room_a,
        date=datetime(2025, 11, 24, tzinfo=timezone.utc).date(),
        start_time=time(9, 0),
        end_time=time(12, 0),
        used_capacity=10,
    )

    # Room B
    Reservation.objects.create(
        resource=room_b,
        date=datetime(2025, 11, 23, tzinfo=timezone.utc).date(),
        start_time=time(10, 0),
        end_time=time(12, 0),
        used_capacity=5,
    )
    Reservation.objects.create(
        resource=room_b,
        date=datetime(2025, 11, 24, tzinfo=timezone.utc).date(),
        start_time=time(13, 0),
        end_time=time(15, 0),
        used_capacity=10,
    )

    # Create vehicle reservations
    Reservation.objects.create(
        resource=vehicle_a,
        date=datetime(2025, 11, 23, tzinfo=timezone.utc).date(),
        start_time=time(0, 0),
        end_time=time(23, 59),
    )
    Reservation.objects.create(
        resource=vehicle_b,
        date=datetime(2025, 11, 24, tzinfo=timezone.utc).date(),
        start_time=time(0, 0),
        end_time=time(23, 59),
    )

    # Equipment reservations
    # Projector
    Reservation.objects.create(
        resource=projector,
        date=datetime(2025, 11, 23, tzinfo=timezone.utc).date(),
        start_time=time(10, 0),
        end_time=time(12, 0),
    )
    Reservation.objects.create(
        resource=projector,
        date=datetime(2025, 11, 23, tzinfo=timezone.utc).date(),
        start_time=time(15, 0),
        end_time=time(18, 0),
    )
    Reservation.objects.create(
        resource=projector,
        date=datetime(2025, 11, 24, tzinfo=timezone.utc).date(),
        start_time=time(10, 0),
        end_time=time(12, 0),
    )
    Reservation.objects.create(
        resource=projector,
        date=datetime(2025, 11, 24, tzinfo=timezone.utc).date(),
        start_time=time(14, 0),
        end_time=time(16, 0),
    )
    Reservation.objects.create(
        resource=projector,
        date=datetime(2025, 11, 26, tzinfo=timezone.utc).date(),
        start_time=time(8, 0),
        end_time=time(20, 0),
    )

    # Whiteboard
    Reservation.objects.create(
        resource=whiteboard,
        date=datetime(2025, 11, 23, tzinfo=timezone.utc).date(),
        start_time=time(9, 0),
        end_time=time(11, 0),
    )
    Reservation.objects.create(
        resource=whiteboard,
        date=datetime(2025, 11, 24, tzinfo=timezone.utc).date(),
        start_time=time(13, 0),
        end_time=time(15, 0),
    )
    Reservation.objects.create(
        resource=whiteboard,
        date=datetime(2025, 11, 25, tzinfo=timezone.utc).date(),
        start_time=time(10, 0),
        end_time=time(12, 0),
    )
    Reservation.objects.create(
        resource=whiteboard,
        date=datetime(2025, 11, 26, tzinfo=timezone.utc).date(),
        start_time=time(14, 0),
        end_time=time(18, 0),
    )

    print("Resources seeded successfully!")


if __name__ == "__main__":
    run()
