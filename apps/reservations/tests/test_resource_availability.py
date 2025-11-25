from datetime import time
from rest_framework.test import APITestCase
from .conftest import ReservationTestSetup


class ResourceAvailabilityTest(ReservationTestSetup, APITestCase):
    """Tests for the resource availability API endpoint using fixture data."""

    # Meeting Room Tests
    def test_meeting_room_full_capacity(self):
        result = self.service.execute(
            resource_id=self.meeting_room.id,
            date="2025-11-23",
            start_time=time(14, 0),
            end_time=time(16, 0),
        )
        self.assertFalse(result["available"])
        self.assertEqual(result["capacity_remaining"], 0)
        self.assertEqual(len(result["blocking_reservations"]), 2)

    def test_meeting_room_partial_capacity(self):
        result = self.service.execute(
            resource_id=self.meeting_room.id,
            date="2025-11-24",
            start_time=time(9, 0),
            end_time=time(10, 0),
        )
        self.assertTrue(result["available"])
        self.assertEqual(result["capacity_remaining"], 9)

    def test_meeting_room_free_slot(self):
        result = self.service.execute(
            resource_id=self.meeting_room.id,
            date="2025-11-23",
            start_time=time(11, 0),
            end_time=time(14, 0),
        )
        self.assertTrue(result["available"])
        self.assertEqual(result["capacity_remaining"], 20)
        self.assertEqual(len(result["blocking_reservations"]), 0)

    def test_meeting_room_partial_overlap(self):
        result = self.service.execute(
            resource_id=self.meeting_room.id,
            date="2025-11-23",
            start_time=time(10, 0),
            end_time=time(15, 0),
        )
        self.assertFalse(result["available"])
        self.assertEqual(result["capacity_remaining"], 0)
        self.assertGreaterEqual(len(result["blocking_reservations"]), 1)

    # Vehicle Tests
    def test_vehicle_full_day_blocked(self):
        """Vehicle unavailable when reserved for the full day"""
        result = self.service.execute(
            resource_id=self.vehicle.id,
            date="2025-11-23",
        )
        self.assertFalse(result["available"])
        self.assertEqual(len(result["blocking_reservations"]), 1)

    def test_vehicle_free_day(self):
        """Vehicle available on a day without reservations"""
        result = self.service.execute(
            resource_id=self.vehicle.id,
            date="2025-11-25",  # día sin reservas
        )
        self.assertTrue(result["available"])
        self.assertEqual(len(result["blocking_reservations"]), 0)

    def test_vehicle_multiple_reservations_same_day(self):
        """Vehicle unavailable when multiple reservations exist on the same day"""
        result = self.service.execute(
            resource_id=self.vehicle.id,
            date="2025-11-24",
        )
        self.assertFalse(result["available"])
        self.assertEqual(len(result["blocking_reservations"]), 2)

    # Equipment Tests
    def test_equipment_blocked_slot(self):
        """Equipment unavailable on 2025-11-23 between 10:00-18:00."""
        result = self.service.execute(
            resource_id=self.equipment.id,
            date="2025-11-23",
            start_time=time(10, 0),
            end_time=time(16, 0),
        )
        self.assertFalse(result["available"])
        self.assertTrue(len(result["blocking_reservations"]) >= 1)

    def test_equipment_available_partial_day(self):
        """Equipment available on 2025-11-24 for an unreserved time slot."""
        result = self.service.execute(
            resource_id=self.equipment.id,
            date="2025-11-24",
            start_time=time(12, 0),
            end_time=time(14, 0),
        )
        self.assertTrue(result["available"])
        self.assertEqual(result["blocking_reservations"], [])

    def test_equipment_fully_booked_day(self):
        """Equipment unavailable when a full-day reservation exists."""
        result = self.service.execute(
            resource_id=self.equipment.id,
            date="2025-11-26",
            start_time=time(8, 0),
            end_time=time(20, 0),
        )
        self.assertFalse(result["available"])
        self.assertTrue(len(result["blocking_reservations"]) >= 1)

    def test_day_without_reservations(self):
        """All resources should be available on 2025-11-25 with no reservations."""
        for resource in [
            self.meeting_room,
            self.vehicle,
            self.equipment,
        ]:
            result = self.service.execute(
                resource_id=resource.id,
                date="2025-11-25",
            )
            self.assertTrue(result["available"])
            self.assertEqual(result["blocking_reservations"], [])
