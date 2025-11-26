from django.urls import path
from .views import (
    ResourceAvailabilityView,
    CreateReservationView,
    ApproveReservationView,
)

urlpatterns = [
    path(
        "resources/<int:resource_id>/availability/",
        ResourceAvailabilityView.as_view(),
        name="resource-availability",
    ),
    path(
        "resources/<int:resource_id>/reservations/",
        CreateReservationView.as_view(),
        name="resource-reservations",
    ),
    path(
        "reservations/<int:reservation_id>/approve/",
        ApproveReservationView.as_view(),
        name="reservation-approve",
    ),
]
