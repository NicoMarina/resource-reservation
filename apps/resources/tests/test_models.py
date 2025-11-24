from .tests import ResourceTestSetup


class ResourceModelTest(ResourceTestSetup):
    """Tests basic creation and relationship of Resource and MeetingRoom."""

    def test_meeting_room_creation(self):
        self.assertEqual(self.meeting_room.name, "Conference Room A")
        self.assertEqual(self.meeting_room.capacity, 20)
        self.assertEqual(self.meeting_room.description, "A large conference room")

    def test_vehicle_creation(self):
        self.assertEqual(self.vehicle.name, "Company Car")
        self.assertEqual(self.vehicle.description, "A car for business trips")

    def test_equipment_creation(self):
        self.assertEqual(self.equipment.name, "Projector")
        self.assertEqual(self.equipment.description, "HD Projector")
