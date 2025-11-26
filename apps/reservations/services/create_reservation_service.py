from django.db import transaction
from rest_framework.exceptions import ValidationError
from apps.resources.models import Resource
from ..models import Reservation
from .datetime_utils import normalize_reservation_inputs
from .reservation_role_resolver import RoleChecker, ReservationStatusResolver


class CreateReservationService:
    """
    Service to create a reservation with proper availability checks and status handling.
    """

    def execute(
        self,
        resource_id,
        user,
        date,
        start_time=None,
        end_time=None,
        used_capacity=None,
        status="pending",
        approved_by=None,
        created_by=None,
    ):
        resource = Resource.objects.get(id=resource_id)
        date, start_time, end_time = normalize_reservation_inputs(
            date, start_time, end_time
        )
        used_capacity = int(used_capacity or 1)

        role_checker = RoleChecker(user)
        status, approved_by = ReservationStatusResolver(role_checker).get_status()

        with transaction.atomic():
            # Lock reservations for the resource and date
            Reservation.objects.select_for_update().filter(
                resource=resource, date=date
            ).count()

            # Get availability
            availability = resource.check_availability(
                date=date,
                start_time=start_time,
                end_time=end_time,
                used_capacity=used_capacity,
            )

            if (
                not availability.get("available", False)
                and not role_checker.is_manager()
            ):
                # Always return the same structure for errors
                raise ValidationError(
                    {
                        "success": False,
                        "available": False,
                        "reason": availability.get("reason", "Not available"),
                        "blocking_reservations": availability.get(
                            "blocking_reservations", []
                        ),
                    }
                )

            reservation = resource.create_reservation(
                date=date,
                start_time=start_time,
                end_time=end_time,
                used_capacity=(
                    used_capacity if resource.allow_shared_capacity() else None
                ),
                status=status,
                approved_by=approved_by,
                created_by=user,
            )

        return reservation
