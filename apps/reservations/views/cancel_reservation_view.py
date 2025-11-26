from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Reservation
from ..services import CancelReservationService
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class CancelReservationView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, reservation_id):
        reservation = Reservation.objects.get(id=reservation_id)

        service = CancelReservationService()
        result = service.execute(reservation, request.user)

        return Response(
            {
                "success": result["success"],
                "message": result["message"],
                "cancelled": result["cancelled"],
                "transferred_to": result["transferred_to"],
            }
        )
