from rest_framework.exceptions import PermissionDenied, NotFound
from apps.reservations.models import Reservation
from .reservation_policy import RoleChecker


class ApproveReservationService:
    """
    Service to approve a reservation. Only managers can approve.
    """

    def execute(self, user, reservation_id):
        role_checker = RoleChecker(user)
        if not role_checker.is_manager():
            raise PermissionDenied("Only managers can approve reservations")

        try:
            reservation = Reservation.objects.get(id=reservation_id)
        except Reservation.DoesNotExist:
            raise NotFound(f"Reservation {reservation_id} does not exist")

        if reservation.status == "approved":
            return reservation

        reservation.status = "approved"
        reservation.approved_by = user
        reservation.save(update_fields=["status", "approved_by"])
        return reservation
