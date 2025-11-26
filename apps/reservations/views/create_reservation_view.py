# apps/reservations/views/reservation_create_view.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from ..services import CreateReservationService
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class CreateReservationView(APIView):
    """
    API endpoint to create a reservation for any resource.
    Delegates validation to the resource itself via polymorphic check_availability.
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, resource_id):
        service = CreateReservationService()
        reservation = service.execute(
            resource_id=resource_id,
            user=request.user,
            date=request.data.get("date"),
            start_time=request.data.get("start_time"),
            end_time=request.data.get("end_time"),
            used_capacity=request.data.get("used_capacity"),
        )

        if isinstance(reservation, ValidationError):
            raise reservation

        return Response(
            {
                "id": reservation.id,
                "resource_id": reservation.resource.id,
                "date": str(reservation.date),
                "start_time": (
                    str(reservation.start_time) if reservation.start_time else None
                ),
                "end_time": str(reservation.end_time) if reservation.end_time else None,
                "used_capacity": reservation.used_capacity,
                "status": reservation.status,
                "approved_by": (
                    reservation.approved_by.username
                    if reservation.approved_by
                    else None
                ),
            },
            status=status.HTTP_201_CREATED,
        )
