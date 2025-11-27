from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.reservations.models import Reservation
from .conftest import ReservationTestSetup
from django.utils import timezone
from datetime import timedelta, datetime, time

User = get_user_model()


class ReservationAPIIntegrationTests(ReservationTestSetup, APITestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        # Future date reservations for cancellation tests
        cls.future_date = timezone.now().date() + timedelta(days=1)
        cls.start_time = (timezone.now() + timedelta(hours=2)).time()
        cls.end_time = (
            datetime.combine(cls.future_date, cls.start_time) + timedelta(hours=1)
        ).time()

        # Flexible MeetingRoom reservation
        cls.approved_room_res = Reservation.objects.create(
            resource=cls.meeting_room,
            date=cls.future_date,
            start_time=cls.start_time,
            end_time=cls.end_time,
            status="approved",
            created_by=cls.manager,
            approved_by=cls.manager,
        )
        cls.pending_room_res = Reservation.objects.create(
            resource=cls.meeting_room,
            date=cls.future_date,
            start_time=cls.start_time,
            end_time=cls.end_time,
            status="pending",
            created_by=cls.user,
        )

        # Moderate Vehicle reservation
        cls.approved_vehicle_res = Reservation.objects.create(
            resource=cls.vehicle,
            date=cls.future_date + timedelta(days=1),
            start_time=time(9, 0),
            end_time=time(18, 0),
            status="approved",
            created_by=cls.manager,
            approved_by=cls.manager,
        )

        # Blocked Equipment reservation
        cls.approved_equip_res = Reservation.objects.create(
            resource=cls.equipment,
            date=cls.future_date,
            start_time=time(10, 0),
            end_time=time(12, 0),
            status="approved",
            created_by=cls.manager,
            approved_by=cls.manager,
        )

    # Authentication helpers
    def auth_as_worker(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.worker_token.key}")

    def auth_as_manager(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.manager_token.key}")

    # Availability
    def test_resource_availability(self):
        """Verifica que la API de availability devuelve el estado correcto."""
        self.auth_as_worker()

        url = (
            f"/api/resources/{self.meeting_room.id}/availability/"
            f"?date=2025-11-23&start_time=11:00&end_time=12:00"
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("available", response.data)
        self.assertIn("free_hours", response.data)

    # Creation
    def test_worker_creates_pending_meeting_room(self):
        """Worker crea una reserva válida de MeetingRoom → pending"""
        self.auth_as_worker()

        data = {
            "date": "2025-11-23",
            "start_time": "11:00",
            "end_time": "12:00",
            "used_capacity": 5,
        }
        url = f"/api/resources/{self.meeting_room.id}/reservations/"
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["status"], "pending")

    def test_manager_creates_approved_meeting_room(self):
        """Manager crea reserva de MeetingRoom válida → approved"""
        self.auth_as_manager()

        data = {
            "date": "2025-11-23",
            "start_time": "11:00",
            "end_time": "12:00",
            "used_capacity": 5,
        }
        url = f"/api/resources/{self.meeting_room.id}/reservations/"
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["status"], "approved")

    def test_worker_vehicle_pending_on_free_day(self):
        """Worker reserva un vehículo en día libre → pending"""
        self.auth_as_worker()

        data = {"date": "2025-11-25"}
        url = f"/api/resources/{self.vehicle.id}/reservations/"
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["status"], "pending")

    def test_manager_vehicle_approve_on_conflict(self):
        """Manager puede reservar vehículo aun con conflicto → approved"""
        self.auth_as_manager()

        data = {"date": "2025-11-24"}
        url = f"/api/resources/{self.vehicle.id}/reservations/"
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["status"], "approved")

    def test_worker_equipment_hourly_reservation(self):
        """Worker crea reserva de equipo por horas → pending"""
        self.auth_as_worker()

        data = {"date": "2025-11-25", "start_time": "10:00", "end_time": "12:00"}
        url = f"/api/resources/{self.equipment.id}/reservations/"
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["status"], "pending")

    def test_manager_equipment_conflict_override(self):
        """Manager puede crear reserva de equipo aunque haya solapamiento → approved"""
        self.auth_as_manager()

        data = {"date": "2025-11-23", "start_time": "12:00", "end_time": "14:00"}
        url = f"/api/resources/{self.equipment.id}/reservations/"
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["status"], "approved")

    # Approve
    def test_manager_approve_pending_reservation(self):
        """Manager aprueba reserva pendiente manualmente"""
        self.auth_as_manager()

        url = f"/api/reservations/{self.room_res2.id}/approve/"
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.room_res2.refresh_from_db()
        self.assertEqual(self.room_res2.status, "approved")

    # Cancel
    def test_cancel_blocked_policy_reservation(self):
        """Blocked → 403 Forbidden"""
        self.auth_as_worker()
        url = f"/api/reservations/{self.approved_equip_res.id}/cancel/"
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cancel_flexible_reservation(self):
        """Flexible → 200 OK, pending approved"""
        self.auth_as_manager()
        url = f"/api/reservations/{self.approved_room_res.id}/cancel/"
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.approved_room_res.refresh_from_db()
        self.pending_room_res.refresh_from_db()
        self.assertEqual(self.approved_room_res.status, "cancelled")
        self.assertEqual(self.pending_room_res.status, "approved")
        self.assertEqual(
            self.pending_room_res.approved_by, self.approved_room_res.approved_by
        )

    def test_cancel_moderate_reservation_within_limit(self):
        """Moderate, >24h ahead → 200 OK"""
        self.auth_as_manager()
        self.approved_vehicle_res.date = timezone.now().date() + timedelta(days=2)
        self.approved_vehicle_res.save()

        url = f"/api/reservations/{self.approved_vehicle_res.id}/cancel/"
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.approved_vehicle_res.refresh_from_db()
        self.assertEqual(self.approved_vehicle_res.status, "cancelled")

    def test_cancel_moderate_reservation_too_late(self):
        """Moderate, <24h → 403 Forbidden"""
        self.auth_as_manager()
        self.approved_vehicle_res.date = timezone.now().date()
        self.approved_vehicle_res.save()

        url = f"/api/reservations/{self.approved_vehicle_res.id}/cancel/"
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)