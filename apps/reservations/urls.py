from django.urls import path
from .views import ResourceAvailabilityView

urlpatterns = [
    path(
        "resources/<int:resource_id>/availability/",
        ResourceAvailabilityView.as_view(),
        name="resource-availability",
    )
]
