from rest_framework.exceptions import APIException
from django.utils import timezone
from apps.reservations.models.reservation import Reservation
from apps.reservations.services.availability_utils import overlaps


class CancelReservationService:
    """
    Handles cancellation of a reservation according to the resource's
    cancellation policy and automatically approves pending reservations
    in the same slot if applicable.
    """

    def execute(self, reservation: Reservation, user):
        # Check cancellation policy
        if not reservation.resource.cancellation_policy.can_cancel(reservation, user):
            raise APIException("Cannot cancel reservation due to policy.")

        reservations = Reservation.objects.filter(
            resource=reservation.resource, date=reservation.date
        ).exclude(id=reservation.id)

        overlapping_pending = [
            r
            for r in reservations
            if r.status == "pending"
            and overlaps(
                r.start_time, r.end_time, reservation.start_time, reservation.end_time
            )
        ]

        transferred = None
        if overlapping_pending:
            # Approve the first overlapping slope
            next_pending = sorted(overlapping_pending, key=lambda r: r.id)[0]
            next_pending.status = "approved"
            next_pending.approved_by = (
                reservation.approved_by
            )
            next_pending.save()
            transferred = next_pending

        # Cancel current reservation.
        reservation.status = "cancelled"
        reservation.cancelled = True
        reservation.save()

        return {
            "success": True,
            "message": (
                "Reservation cancelled successfully."
                if not transferred
                else "Reservation cancelled successfully. Pending reservation approved."
            ),
            "cancelled": reservation.id,
            "transferred_to": transferred.id if transferred else None,
        }
