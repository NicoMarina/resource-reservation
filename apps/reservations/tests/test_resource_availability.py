from datetime import time
from rest_framework.test import APITestCase
from .conftest import ReservationTestSetup


class ResourceAvailabilityTest(ReservationTestSetup, APITestCase):
    """Tests for resource availability API endpoint with pending reservations handled."""

    # Meeting Room
    def test_meeting_room_full_capacity(self):
        """Room is unavailable only if approved reservations fill capacity."""
        result = self.availability_service.execute(
            resource_id=self.meeting_room.id,
            date="2025-11-23",
            start_time=time(15, 0),
            end_time=time(16, 0),
        )
        self.assertTrue(result["available"])
        self.assertEqual(result["capacity_remaining"], 10)
        self.assertEqual(len(result["blocking_reservations"]), 1)
        self.assertEqual(len(result["pending_reservations"]), 1)

    def test_meeting_room_partial_capacity(self):
        """Room allows reservation if approved reservations do not fill capacity."""
        result = self.availability_service.execute(
            resource_id=self.meeting_room.id,
            date="2025-11-24",
            start_time=time(9, 0),
            end_time=time(10, 0),
        )
        self.assertTrue(result["available"])
        self.assertEqual(result["capacity_remaining"], 19)
        self.assertEqual(len(result["blocking_reservations"]), 1)
        self.assertEqual(len(result["pending_reservations"]), 1)

    def test_meeting_room_free_slot(self):
        """Room is fully available when no approved reservations overlap."""
        result = self.availability_service.execute(
            resource_id=self.meeting_room.id,
            date="2025-11-23",
            start_time=time(11, 0),
            end_time=time(14, 0),
        )
        self.assertTrue(result["available"])
        self.assertEqual(result["capacity_remaining"], 20)
        self.assertEqual(len(result["blocking_reservations"]), 0)
        self.assertEqual(len(result["pending_reservations"]), 0)

    def test_meeting_room_partial_overlap(self):
        """Partial overlap with approved reservations reduces availability."""
        result = self.availability_service.execute(
            resource_id=self.meeting_room.id,
            date="2025-11-23",
            start_time=time(10, 0),
            end_time=time(15, 0),
        )
        self.assertTrue(result["available"])
        self.assertEqual(result["capacity_remaining"], 10)
        self.assertGreaterEqual(len(result["blocking_reservations"]), 1)
        self.assertEqual(len(result["pending_reservations"]), 1)

    # Vehicle
    def test_vehicle_full_day_blocked(self):
        result = self.availability_service.execute(
            resource_id=self.vehicle.id,
            date="2025-11-23",
        )
        self.assertFalse(result["available"])
        self.assertEqual(len(result["blocking_reservations"]), 1)
        self.assertEqual(len(result["pending_reservations"]), 0)

    def test_vehicle_free_day(self):
        result = self.availability_service.execute(
            resource_id=self.vehicle.id,
            date="2025-11-25",
        )
        self.assertTrue(result["available"])
        self.assertEqual(len(result["blocking_reservations"]), 0)
        self.assertEqual(len(result["pending_reservations"]), 0)

    def test_vehicle_multiple_reservations_same_day(self):
        result = self.availability_service.execute(
            resource_id=self.vehicle.id,
            date="2025-11-24",
        )
        self.assertFalse(result["available"])
        self.assertEqual(len(result["blocking_reservations"]), 1)
        self.assertEqual(len(result["pending_reservations"]), 1)

    # Equipment
    def test_equipment_blocked_slot(self):
        result = self.availability_service.execute(
            resource_id=self.equipment.id,
            date="2025-11-23",
            start_time=time(10, 0),
            end_time=time(16, 0),
        )
        self.assertFalse(result["available"])
        self.assertGreaterEqual(len(result["blocking_reservations"]), 1)
        self.assertEqual(len(result["pending_reservations"]), 1)

    def test_equipment_available_partial_day(self):
        result = self.availability_service.execute(
            resource_id=self.equipment.id,
            date="2025-11-24",
            start_time=time(12, 0),
            end_time=time(14, 0),
        )
        self.assertTrue(result["available"])
        self.assertEqual(result["blocking_reservations"], [])
        self.assertEqual(len(result["pending_reservations"]), 0)

    def test_equipment_fully_booked_day(self):
        result = self.availability_service.execute(
            resource_id=self.equipment.id,
            date="2025-11-26",
            start_time=time(8, 0),
            end_time=time(20, 0),
        )
        self.assertFalse(result["available"])
        self.assertGreaterEqual(len(result["blocking_reservations"]), 1)
        self.assertEqual(len(result["pending_reservations"]), 0)

    def test_day_without_reservations(self):
        for resource in [self.meeting_room, self.vehicle, self.equipment]:
            result = self.availability_service.execute(
                resource_id=resource.id,
                date="2025-11-25",
            )
            self.assertTrue(result["available"])
            self.assertEqual(result["blocking_reservations"], [])
            self.assertEqual(result["pending_reservations"], [])
