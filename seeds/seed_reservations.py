import os
import django
from datetime import datetime, time, timedelta, timezone as dt_timezone
from django.utils import timezone


# Configure Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "resource_reservation.settings")
django.setup()

from apps.resources.models import MeetingRoom, Vehicle, Equipment
from apps.reservations.models import Reservation
from django.contrib.auth.models import User


def run():
    # Clean up existing data
    Reservation.objects.all().delete()

    # Get users
    worker = User.objects.get(username="worker1")
    manager = User.objects.get(username="manager1")

    # Get resources
    rooms = MeetingRoom.objects.all()
    vehicles = Vehicle.objects.all()
    equipments = Equipment.objects.all()

    room_a, room_b = rooms[0], rooms[1]
    vehicle_a, vehicle_b = vehicles[0], vehicles[1]
    projector, whiteboard = equipments[0], equipments[1]

    date = timezone.now().date() + timedelta(days=1)

    # Examples for cancelling reservations
    res1 = Reservation.objects.create(
        resource=room_a,
        date=date,
        start_time=time(10, 0),
        end_time=time(11, 0),
        used_capacity=10,
        status="approved",
        approved_by=manager,
        created_by=worker,
    )

    res2 = Reservation.objects.create(
        resource=room_a,
        date=date,
        start_time=time(10, 0),
        end_time=time(11, 0),
        used_capacity=3,
        status="pending",
        created_by=worker,
    )

    res3 = Reservation.objects.create(
        resource=projector,
        date=date,
        start_time=time(10, 0),
        end_time=time(11, 0),
        status="approved",
        approved_by=manager,
        created_by=worker,
    )

    res4 = Reservation.objects.create(
        resource=projector,
        date=date,
        start_time=time(10, 0),
        end_time=time(11, 0),
        status="pending",
        created_by=worker,
    )

    res5 = Reservation.objects.create(
        resource=vehicle_a,
        date=date,
        start_time=time(9, 0),
        end_time=time(10, 0),
        status="approved",
        approved_by=manager,
        created_by=worker,
    )

    res6 = Reservation.objects.create(
        resource=vehicle_b,
        date=timezone.now().date(),
        start_time=(timezone.now() + timedelta(hours=2)).time(),
        end_time=(timezone.now() + timedelta(hours=3)).time(),
        status="approved",
        approved_by=manager,
        created_by=worker,
    )

    # Create meeting rooms reservations
    # Room A
    Reservation.objects.create(
        resource=room_a,
        date=datetime(2025, 11, 23, tzinfo=dt_timezone.utc).date(),
        start_time=time(9, 0),
        end_time=time(11, 0),
        used_capacity=10,
        status="approved",
        approved_by=manager,
        created_by=worker,
    )
    Reservation.objects.create(
        resource=room_a,
        date=datetime(2025, 11, 23, tzinfo=dt_timezone.utc).date(),
        start_time=time(14, 0),
        end_time=time(16, 0),
        used_capacity=20,
        status="approved",
        approved_by=manager,
        created_by=worker,
    )
    Reservation.objects.create(
        resource=room_a,
        date=datetime(2025, 11, 23, tzinfo=dt_timezone.utc).date(),
        start_time=time(15, 0),
        end_time=time(16, 0),
        used_capacity=10,
        status="pending",
        created_by=worker,
    )
    Reservation.objects.create(
        resource=room_a,
        date=datetime(2025, 11, 24, tzinfo=dt_timezone.utc).date(),
        start_time=time(9, 0),
        end_time=time(10, 0),
        used_capacity=1,
        status="approved",
        approved_by=manager,
        created_by=worker,
    )
    Reservation.objects.create(
        resource=room_a,
        date=datetime(2025, 11, 24, tzinfo=dt_timezone.utc).date(),
        start_time=time(9, 0),
        end_time=time(12, 0),
        used_capacity=10,
        status="pending",
        created_by=worker,
    )

    # Room B
    Reservation.objects.create(
        resource=room_b,
        date=datetime(2025, 11, 23, tzinfo=dt_timezone.utc).date(),
        start_time=time(10, 0),
        end_time=time(12, 0),
        used_capacity=5,
        status="approved",
        approved_by=manager,
        created_by=worker,
    )
    Reservation.objects.create(
        resource=room_b,
        date=datetime(2025, 11, 24, tzinfo=dt_timezone.utc).date(),
        start_time=time(13, 0),
        end_time=time(15, 0),
        used_capacity=10,
        status="pending",
        created_by=worker,
    )

    # Create vehicle reservations
    Reservation.objects.create(
        resource=vehicle_a,
        date=datetime(2025, 11, 23, tzinfo=dt_timezone.utc).date(),
        status="approved",
        approved_by=manager,
        created_by=worker,
    )
    Reservation.objects.create(
        resource=vehicle_b,
        date=datetime(2025, 11, 24, tzinfo=dt_timezone.utc).date(),
        status="pending",
        created_by=worker,
    )

    # Equipment reservations
    # Projector
    Reservation.objects.create(
        resource=projector,
        date=datetime(2025, 11, 23, tzinfo=dt_timezone.utc).date(),
        start_time=time(10, 0),
        end_time=time(12, 0),
        status="approved",
        approved_by=manager,
        created_by=worker,
    )
    Reservation.objects.create(
        resource=projector,
        date=datetime(2025, 11, 23, tzinfo=dt_timezone.utc).date(),
        start_time=time(15, 0),
        end_time=time(18, 0),
        status="pending",
        created_by=worker,
    )
    Reservation.objects.create(
        resource=projector,
        date=datetime(2025, 11, 24, tzinfo=dt_timezone.utc).date(),
        start_time=time(10, 0),
        end_time=time(12, 0),
        status="approved",
        approved_by=manager,
        created_by=worker,
    )
    Reservation.objects.create(
        resource=projector,
        date=datetime(2025, 11, 24, tzinfo=dt_timezone.utc).date(),
        start_time=time(14, 0),
        end_time=time(16, 0),
        status="pending",
        created_by=worker,
    )
    Reservation.objects.create(
        resource=projector,
        date=datetime(2025, 11, 26, tzinfo=dt_timezone.utc).date(),
        start_time=time(8, 0),
        end_time=time(20, 0),
        status="pending",
        created_by=worker,
    )

    # Whiteboard
    Reservation.objects.create(
        resource=whiteboard,
        date=datetime(2025, 11, 23, tzinfo=dt_timezone.utc).date(),
        start_time=time(9, 0),
        end_time=time(11, 0),
        status="approved",
        approved_by=manager,
        created_by=worker,
    )
    Reservation.objects.create(
        resource=whiteboard,
        date=datetime(2025, 11, 24, tzinfo=dt_timezone.utc).date(),
        start_time=time(13, 0),
        end_time=time(15, 0),
        status="pending",
        created_by=worker,
    )
    Reservation.objects.create(
        resource=whiteboard,
        date=datetime(2025, 11, 25, tzinfo=dt_timezone.utc).date(),
        start_time=time(10, 0),
        end_time=time(12, 0),
        status="approved",
        approved_by=manager,
        created_by=worker,
    )
    Reservation.objects.create(
        resource=whiteboard,
        date=datetime(2025, 11, 26, tzinfo=dt_timezone.utc).date(),
        start_time=time(14, 0),
        end_time=time(18, 0),
        status="pending",
        created_by=worker,
    )

    print("Reservations seeded successfully!")


if __name__ == "__main__":
    run()
