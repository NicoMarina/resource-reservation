from django.test import TestCase
from apps.resources.tests import ResourceTestSetup
from ..models import Reservation
from ..services import CheckAvailabilityService, CreateReservationService
from datetime import datetime, time, timezone
from django.contrib.auth import get_user_model

User = get_user_model()


class ReservationTestSetup(ResourceTestSetup):
    """Sets up test data for reservation-related tests."""

    @classmethod
    def setUpTestData(cls):
        # Execute the parent class's setUpTestData to create resources
        super().setUpTestData()

        cls.user = User.objects.create_user(username="worker", password="password123")
        cls.manager = User.objects.create_user(
            username="manager", password="password123"
        )
        cls.manager.groups.create(name="manager")

        # MeetingRoom reservations
        cls.room_res1 = Reservation.objects.create(
            resource=cls.meeting_room,
            date=datetime(2025, 11, 23, tzinfo=timezone.utc).date(),
            start_time=time(9, 0),
            end_time=time(11, 0),
            used_capacity=10,
            status="approved",
            created_by=cls.manager,
        )
        cls.room_res2 = Reservation.objects.create(
            resource=cls.meeting_room,
            date=datetime(2025, 11, 23, tzinfo=timezone.utc).date(),
            start_time=time(14, 0),
            end_time=time(16, 0),
            used_capacity=10,
            status="pending",
            created_by=cls.user,
        )
        cls.room_res3 = Reservation.objects.create(
            resource=cls.meeting_room,
            date=datetime(2025, 11, 23, tzinfo=timezone.utc).date(),
            start_time=time(15, 0),
            end_time=time(16, 0),
            used_capacity=10,
            status="approved",
            created_by=cls.manager,
        )
        cls.room_res4 = Reservation.objects.create(
            resource=cls.meeting_room,
            date=datetime(2025, 11, 24, tzinfo=timezone.utc).date(),
            start_time=time(9, 0),
            end_time=time(10, 0),
            used_capacity=1,
            status="approved",
            created_by=cls.manager,
        )
        cls.room_res5 = Reservation.objects.create(
            resource=cls.meeting_room,
            date=datetime(2025, 11, 24, tzinfo=timezone.utc).date(),
            start_time=time(9, 0),
            end_time=time(12, 0),
            used_capacity=10,
            status="pending",
            created_by=cls.user,
        )

        # Vehicle reservation
        cls.vehicle_res1 = Reservation.objects.create(
            resource=cls.vehicle,
            date=datetime(2025, 11, 23, tzinfo=timezone.utc).date(),
            start_time=time(0, 0),
            end_time=time(23, 59),
            status="approved",
            created_by=cls.manager,
        )
        cls.vehicle_res2 = Reservation.objects.create(
            resource=cls.vehicle,
            date=datetime(2025, 11, 24, tzinfo=timezone.utc).date(),
            start_time=time(0, 0),
            end_time=time(23, 59),
            status="pending",
            created_by=cls.user,
        )
        cls.vehicle_res3 = Reservation.objects.create(
            resource=cls.vehicle,
            date=datetime(2025, 11, 24, tzinfo=timezone.utc).date(),
            start_time=time(0, 0),
            end_time=time(23, 59),
            status="approved",
        )

        # Equipment reservations
        cls.equip_res1 = Reservation.objects.create(
            resource=cls.equipment,
            date=datetime(2025, 11, 23, tzinfo=timezone.utc).date(),
            start_time=time(10, 0),
            end_time=time(12, 0),
            status="approved",
            created_by=cls.manager,
        )
        cls.equip_res2 = Reservation.objects.create(
            resource=cls.equipment,
            date=datetime(2025, 11, 23, tzinfo=timezone.utc).date(),
            start_time=time(15, 0),
            end_time=time(18, 0),
            status="pending",
            created_by=cls.user,
        )
        cls.equip_res3 = Reservation.objects.create(
            resource=cls.equipment,
            date=datetime(2025, 11, 24, tzinfo=timezone.utc).date(),
            start_time=time(10, 0),
            end_time=time(12, 0),
            status="approved",
            created_by=cls.manager,
        )
        cls.equip_res4 = Reservation.objects.create(
            resource=cls.equipment,
            date=datetime(2025, 11, 24, tzinfo=timezone.utc).date(),
            start_time=time(14, 0),
            end_time=time(16, 0),
            status="pending",
            created_by=cls.user,
        )
        cls.equip_res5 = Reservation.objects.create(
            resource=cls.equipment,
            date=datetime(2025, 11, 26, tzinfo=timezone.utc).date(),
            start_time=time(8, 0),
            end_time=time(20, 0),
            status="approved",
            created_by=cls.manager,
        )

        # Initialize the CheckAvailabilityService
        cls.availability_service = CheckAvailabilityService()
        cls.create_service = CreateReservationService()
