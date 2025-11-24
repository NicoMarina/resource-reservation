from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Resource
from ..serializers import ResourceSerializer


class ResourceListView(APIView):
    """
    List all resources.
    """

    def get(self, request):
        resources = Resource.objects.all().order_by("name")
        serializer = ResourceSerializer(resources, many=True)
        return Response(serializer.data)
