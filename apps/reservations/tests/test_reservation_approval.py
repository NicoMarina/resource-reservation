from django.test import TestCase
from rest_framework.exceptions import PermissionDenied, NotFound
from ..services.approve_reservation_service import ApproveReservationService
from .conftest import ReservationTestSetup  # tu fixture base


class ApproveReservationServiceTests(ReservationTestSetup):

    def setUp(self):
        self.service = ApproveReservationService()

    def test_worker_cannot_approve_pending(self):
        with self.assertRaises(PermissionDenied):
            self.service.execute(self.user, self.room_res2.id)  # worker intenta aprobar

    def test_manager_can_approve_pending(self):
        reservation = self.service.execute(self.manager, self.room_res2.id)
        self.assertEqual(reservation.status, "approved")
        self.assertEqual(reservation.approved_by, self.manager)

    def test_manager_cannot_approve_already_approved(self):
        reservation = self.service.execute(
            self.manager, self.room_res1.id
        )  # ya approved
        self.assertEqual(reservation.status, "approved")
        self.assertEqual(reservation.approved_by, self.room_res1.approved_by)

    def test_approve_nonexistent_reservation(self):
        with self.assertRaises(NotFound):
            self.service.execute(self.manager, 999999)
