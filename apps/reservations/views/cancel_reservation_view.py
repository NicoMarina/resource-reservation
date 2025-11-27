from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import APIException
from ..models import Reservation
from ..services import CancelReservationService


class CancelReservationView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, reservation_id):
        reservation = Reservation.objects.get(id=reservation_id)
        service = CancelReservationService()

        try:
            result = service.execute(reservation, request.user)
        except APIException as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)

        return Response(
            {
                "success": result["success"],
                "message": result["message"],
                "status": reservation.status,  # usa status en vez de cancelled
                "transferred_to": result["transferred_to"],
            },
            status=status.HTTP_200_OK,
        )
