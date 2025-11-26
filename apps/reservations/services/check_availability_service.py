from django.shortcuts import get_object_or_404
from apps.resources.models import Resource
from apps.common.utils import normalize_reservation_inputs


class CheckAvailabilityService:
    """Service to check resource availability for any type of resource."""

    def execute(
        self, resource_id, date, start_time=None, end_time=None, used_capacity=None
    ):
        resource = get_object_or_404(Resource, id=resource_id)
        date, start_time, end_time = normalize_reservation_inputs(
            date, start_time, end_time
        )
        return resource.check_availability(date, start_time, end_time)
