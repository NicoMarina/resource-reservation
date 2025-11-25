from django.urls import path
from .views import ResourceAvailabilityView, CreateReservationView

urlpatterns = [
    path(
        "resources/<int:resource_id>/availability/",
        ResourceAvailabilityView.as_view(),
        name="resource-availability",
    ),
    path(
        "resources/<int:resource_id>/reserve/",
        CreateReservationView.as_view(),
        name="resource-reserve",
    ),
]
