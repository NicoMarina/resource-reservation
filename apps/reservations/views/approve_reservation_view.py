from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from ..services import ApproveReservationService


class ApproveReservationView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, reservation_id):
        service = ApproveReservationService()
        reservation = service.execute(request.user, reservation_id)
        return Response(
            {
                "reservation_id": reservation.id,
                "status": reservation.status,
                "approved_by": reservation.approved_by.username,
            },
            status=status.HTTP_200_OK,
        )
