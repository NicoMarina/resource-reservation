from rest_framework import status
from django.urls import reverse
from .conftest import ReservationTestSetup
from datetime import time, datetime, timezone
from ..models import Reservation


class ReservationEndpointTests(ReservationTestSetup):
    """Tests for the reservation creation endpoint."""

    def test_valid_meeting_room_reservation(self):
        """Crear una reserva válida que no supere capacidad ni se solape"""
        url = f"/api/resources/{self.meeting_room.id}/reserve/"
        data = {
            "date": "2025-11-23",
            "start_time": "11:00",
            "end_time": "12:00",
            "used_capacity": 5,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Reservation.objects.filter(
                resource=self.meeting_room, start_time=time(11, 0), end_time=time(12, 0)
            ).exists()
        )

    def test_meeting_room_capacity_exceeded(self):
        """Intentar reservar más capacidad de la disponible"""
        url = f"/api/resources/{self.meeting_room.id}/reserve/"
        data = {
            "date": "2025-11-23",
            "start_time": "9:30",
            "end_time": "10:30",
            "used_capacity": 15,  # Ya hay 10 reservados a esa hora
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("reason", response.data)

    def test_meeting_room_out_of_hours(self):
        """No se puede reservar fuera del horario de oficina"""
        url = f"/api/resources/{self.meeting_room.id}/reserve/"
        data = {
            "date": "2025-11-23",
            "start_time": "02:00",
            "end_time": "03:00",
            "used_capacity": 5,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("reason", response.data)

    def test_vehicle_reservation_conflict(self):
        """Reserva de vehículo falla si ya hay otra el mismo día"""
        # Crear reserva existente
        Reservation.objects.create(
            resource=self.vehicle,
            date=datetime(2025, 11, 24, tzinfo=timezone.utc).date(),
            start_time=time(0, 0),
            end_time=time(23, 59),
        )
        url = f"/api/resources/{self.vehicle.id}/reserve/"
        data = {"date": "2025-11-24"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("reason", response.data)

    def test_valid_vehicle_reservation(self):
        """Reserva válida de vehículo en un día libre"""
        url = f"/api/resources/{self.vehicle.id}/reserve/"
        data = {"date": "2025-11-25"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Reservation.objects.filter(
                resource=self.vehicle,
                date=datetime(2025, 11, 25, tzinfo=timezone.utc).date(),
            ).exists()
        )

    def test_equipment_hourly_reservation(self):
        """Crear reserva de equipo por horas, sin solapamiento"""
        url = f"/api/resources/{self.equipment.id}/reserve/"
        data = {"date": "2025-11-25", "start_time": "10:00", "end_time": "12:00"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_equipment_reservation_conflict(self):
        """Reserva de equipo falla si hay solapamiento con otra"""
        url = f"/api/resources/{self.equipment.id}/reserve/"
        data = {"date": "2025-11-23", "start_time": "11:00", "end_time": "16:00"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("blocking_reservations", response.data)
