from rest_framework.views import APIView
from rest_framework.response import Response
from ..services import CheckAvailabilityService
from ..serializers import AvailabilitySerializer


class ResourceAvailabilityView(APIView):
    """API view to list all resources and their availability status."""

    def get(self, request, resource_id):
        date = request.query_params.get("date")
        start_time = request.query_params.get("start_time")
        end_time = request.query_params.get("end_time")

        service = CheckAvailabilityService()
        result = service.execute(resource_id, date, start_time, end_time)

        serializer = AvailabilitySerializer(result)
        return Response(serializer.data)
