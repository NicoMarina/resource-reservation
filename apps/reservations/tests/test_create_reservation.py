from rest_framework import status
from datetime import time, datetime, timezone
from .conftest import ReservationTestSetup
from ..models import Reservation
from ..services import CheckAvailabilityService, CreateReservationService


class ReservationEndpointTestsWithUsers(ReservationTestSetup):
    """Tests for reservation creation respecting availability and user roles."""

    # MEETING ROOMS
    def test_worker_valid_meeting_room_reservation(self):
        """Worker creates a valid meeting room reservation → pending."""
        self.client.force_login(self.user)
        data = {
            "date": "2025-11-23",
            "start_time": "11:00",
            "end_time": "12:00",
            "used_capacity": 5,
        }

        # Check availability first
        availability = self.availability_service.execute(
            self.meeting_room.id,
            data["date"],
            data["start_time"],
            data["end_time"],
            data["used_capacity"],
        )
        self.assertTrue(availability["available"])

        reservation = self.create_service.execute(
            resource_id=self.meeting_room.id,
            user=self.user,
            date=data["date"],
            start_time=data["start_time"],
            end_time=data["end_time"],
            used_capacity=data["used_capacity"],
        )

        self.assertEqual(reservation.status, "pending")
        self.assertEqual(reservation.created_by, self.user)

    def test_manager_valid_meeting_room_reservation(self):
        """Manager creates a valid meeting room reservation → approved."""
        self.client.force_login(self.manager)
        data = {
            "date": "2025-11-23",
            "start_time": "11:00",
            "end_time": "12:00",
            "used_capacity": 5,
        }

        availability = self.availability_service.execute(
            self.meeting_room.id,
            data["date"],
            data["start_time"],
            data["end_time"],
            data["used_capacity"],
        )
        self.assertTrue(availability["available"])

        reservation = self.create_service.execute(
            resource_id=self.meeting_room.id,
            user=self.manager,
            date=data["date"],
            start_time=data["start_time"],
            end_time=data["end_time"],
            used_capacity=data["used_capacity"],
        )

        self.assertEqual(reservation.status, "approved")
        self.assertEqual(reservation.created_by, self.manager)

    # VEHICLES
    def test_worker_vehicle_reservation_free_day(self):
        """Worker reserves a vehicle on a free day → pending."""
        self.client.force_login(self.user)
        data = {"date": "2025-11-25"}

        availability = self.availability_service.execute(self.vehicle.id, data["date"])
        self.assertTrue(availability["available"])

        reservation = self.create_service.execute(
            resource_id=self.vehicle.id, user=self.user, date=data["date"]
        )

        self.assertEqual(reservation.status, "pending")
        self.assertEqual(reservation.created_by, self.user)

    def test_manager_vehicle_reservation_conflict_override(self):
        """Manager can create a vehicle reservation even if there's a conflict."""
        self.client.force_login(self.manager)

        data = {"date": "2025-11-24"}

        availability = self.availability_service.execute(self.vehicle.id, data["date"])
        self.assertFalse(availability["available"])

        reservation = self.create_service.execute(
            resource_id=self.vehicle.id, user=self.manager, date=data["date"]
        )

        self.assertEqual(reservation.status, "approved")
        self.assertEqual(reservation.created_by, self.manager)

    # EQUIPMENT
    def test_worker_equipment_hourly_reservation(self):
        """Worker creates an hourly equipment reservation → pending."""
        self.client.force_login(self.user)
        data = {"date": "2025-11-25", "start_time": "10:00", "end_time": "12:00"}

        availability = self.availability_service.execute(
            self.equipment.id, data["date"], data["start_time"], data["end_time"]
        )
        self.assertTrue(availability["available"])

        reservation = self.create_service.execute(
            resource_id=self.equipment.id,
            user=self.user,
            date=data["date"],
            start_time=data["start_time"],
            end_time=data["end_time"],
        )

        self.assertEqual(reservation.status, "pending")
        self.assertEqual(reservation.created_by, self.user)

    def test_manager_equipment_hourly_reservation(self):
        """Manager creates an hourly equipment reservation → approved."""
        self.client.force_login(self.manager)
        data = {"date": "2025-11-25", "start_time": "10:00", "end_time": "12:00"}

        availability = self.availability_service.execute(
            self.equipment.id, data["date"], data["start_time"], data["end_time"]
        )
        self.assertTrue(availability["available"])

        reservation = self.create_service.execute(
            resource_id=self.equipment.id,
            user=self.manager,
            date=data["date"],
            start_time=data["start_time"],
            end_time=data["end_time"],
        )

        self.assertEqual(reservation.status, "approved")
        self.assertEqual(reservation.created_by, self.manager)

    def test_worker_equipment_conflict(self):
        """Worker fails when overlapping an existing equipment reservation."""
        self.client.force_login(self.user)
        data = {"date": "2025-11-23", "start_time": "11:00", "end_time": "13:00"}

        availability = self.availability_service.execute(
            self.equipment.id, data["date"], data["start_time"], data["end_time"]
        )
        self.assertFalse(availability["available"])

        from rest_framework.exceptions import ValidationError

        # Para crear, sí usamos el ID
        with self.assertRaises(ValidationError):
            self.create_service.execute(
                resource_id=self.equipment.id,
                user=self.user,
                date=data["date"],
                start_time=data["start_time"],
                end_time=data["end_time"],
            )

    def test_manager_equipment_conflict_override(self):
        """Manager can create equipment reservation even if overlapping."""
        self.client.force_login(self.manager)
        data = {"date": "2025-11-23", "start_time": "12:00", "end_time": "14:00"}

        availability = self.availability_service.execute(
            self.equipment.id, data["date"], data["start_time"], data["end_time"]
        )

        reservation = self.create_service.execute(
            resource_id=self.equipment.id,
            user=self.manager,
            date=data["date"],
            start_time=data["start_time"],
            end_time=data["end_time"],
        )

        self.assertEqual(reservation.status, "approved")
        self.assertEqual(reservation.created_by, self.manager)
