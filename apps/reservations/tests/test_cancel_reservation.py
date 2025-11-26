from django.test import TestCase
from django.utils import timezone
from datetime import timedelta, datetime, time
from django.contrib.auth import get_user_model
from rest_framework.exceptions import APIException
from apps.reservations.models import Reservation
from apps.reservations.services.cancel_reservation_service import (
    CancelReservationService,
)
from apps.resources.models import (
    MeetingRoom,
    Vehicle,
    Equipment,
    FlexiblePolicy,
    ModeratePolicy,
    BlockedPolicy,
)

User = get_user_model()


class ReservationCancellationTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.worker = User.objects.create_user(username="worker", password="123")
        cls.manager = User.objects.create_user(username="manager", password="123")
        cls.manager.groups.create(name="manager")

        cls.flexible = FlexiblePolicy.objects.create(name="Flexible")
        cls.moderate = ModeratePolicy.objects.create(name="Moderate")
        cls.blocked = BlockedPolicy.objects.create(name="Blocked")

        # Resources
        cls.room = MeetingRoom.objects.create(
            name="Room A", capacity=10, cancellation_policy=cls.flexible
        )
        cls.vehicle = Vehicle.objects.create(
            name="Vehicle A", cancellation_policy=cls.moderate
        )
        cls.equipment = Equipment.objects.create(
            name="Projector", cancellation_policy=cls.blocked
        )

        cls.cancel_service = CancelReservationService()

        # Future date and time to satisfy cancellation policies
        cls.future_date = timezone.now().date() + timedelta(days=1)
        cls.start_time = (timezone.now() + timedelta(hours=2)).time()
        cls.end_time = (
            datetime.combine(cls.future_date, cls.start_time) + timedelta(hours=1)
        ).time()

        # MeetingRoom reservations
        cls.approved_room_res = Reservation.objects.create(
            resource=cls.room,
            date=cls.future_date,
            start_time=cls.start_time,
            end_time=cls.end_time,
            status="approved",
            created_by=cls.manager,
            approved_by=cls.manager,
        )
        cls.pending_room_res = Reservation.objects.create(
            resource=cls.room,
            date=cls.future_date,
            start_time=cls.start_time,
            end_time=cls.end_time,
            status="pending",
            created_by=cls.worker,
        )

        # Vehicle reservation (ModeratePolicy)
        cls.approved_vehicle_res = Reservation.objects.create(
            resource=cls.vehicle,
            date=cls.future_date + timedelta(days=1),
            start_time=time(9, 0),
            end_time=time(18, 0),
            status="approved",
            created_by=cls.manager,
            approved_by=cls.manager,
        )

        # Equipment reservation (BlockedPolicy)
        cls.approved_equip_res = Reservation.objects.create(
            resource=cls.equipment,
            date=cls.future_date,
            start_time=time(10, 0),
            end_time=time(12, 0),
            status="approved",
            created_by=cls.manager,
            approved_by=cls.manager,
        )

    def test_cancel_pending_reservation(self):
        """Pending reservation can be cancelled (status -> cancelled)."""
        self.cancel_service.execute(reservation=self.pending_room_res, user=self.worker)
        self.pending_room_res.refresh_from_db()
        self.assertTrue(self.pending_room_res.cancelled)
        self.assertEqual(self.pending_room_res.status, "cancelled")

    def test_cancel_approved_reservation_with_pending(self):
        """Approved reservation cancellation approves first overlapping pending."""
        self.cancel_service.execute(
            reservation=self.approved_room_res, user=self.manager
        )
        self.approved_room_res.refresh_from_db()
        self.pending_room_res.refresh_from_db()
        self.assertTrue(self.approved_room_res.cancelled)
        self.assertEqual(self.pending_room_res.status, "approved")
        self.assertEqual(
            self.pending_room_res.approved_by, self.approved_room_res.approved_by
        )

    def test_cancel_approved_reservation_no_pending(self):
        """Approved reservation cancellation leaves slot free if no overlapping pending."""
        # Create approved reservation with no overlap with any pending ones
        start = (timezone.now() + timedelta(hours=4)).time()
        end = (datetime.combine(self.future_date, start) + timedelta(hours=1)).time()
        res = Reservation.objects.create(
            resource=self.room,
            date=self.future_date,
            start_time=start,
            end_time=end,
            status="approved",
            created_by=self.manager,
            approved_by=self.manager,
        )
        self.cancel_service.execute(reservation=res, user=self.manager)
        res.refresh_from_db()
        self.assertTrue(res.cancelled)

    def test_cancel_blocked_policy(self):
        """Blocked policy prevents cancellation."""
        with self.assertRaises(APIException):
            self.cancel_service.execute(
                reservation=self.approved_equip_res, user=self.manager
            )

    def test_cancel_moderate_policy_too_late(self):
        """Moderate policy: cannot cancel within 24h of start_time."""
        # Date less than 24h ahead so it should fail
        res = self.approved_vehicle_res
        res.date = timezone.now().date()
        res.save()
        with self.assertRaises(APIException):
            self.cancel_service.execute(reservation=res, user=self.manager)

    def test_cancel_flexible_policy_within_deadline(self):
        """Flexible policy: can cancel up to 1h before start_time."""
        self.cancel_service.execute(
            reservation=self.approved_room_res, user=self.manager
        )
        self.approved_room_res.refresh_from_db()
        self.assertTrue(self.approved_room_res.cancelled)
