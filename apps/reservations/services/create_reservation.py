from django.db import transaction
from rest_framework.exceptions import ValidationError
from apps.resources.models import Resource
from apps.reservations.models import Reservation
from apps.reservations.services.availability_utils import normalize_reservation_inputs


class CreateReservationService:
    def execute(
        self,
        resource_id,
        date,
        start_time=None,
        end_time=None,
        used_capacity=None,
    ):
        resource = Resource.objects.get(id=resource_id)
        date, start_time, end_time = normalize_reservation_inputs(
            date, start_time, end_time
        )

        with transaction.atomic():
            Reservation.objects.select_for_update().filter(
                resource=resource, date=date
            ).count()

            availability = resource.check_availability(
                date=date,
                start_time=start_time,
                end_time=end_time,
                used_capacity=used_capacity,
            )

            if not availability.get("available", False):
                raise ValidationError(availability)

            # YA VALIDADO → crear reserva sin volver a llamar a check_availability
            reservation = resource.create_reservation(
                date=date,
                start_time=start_time,
                end_time=end_time,
                used_capacity=used_capacity,
            )

        return reservation
