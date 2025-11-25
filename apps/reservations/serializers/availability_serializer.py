from rest_framework import serializers


class AvailabilitySerializer(serializers.Serializer):
    resource_id = serializers.IntegerField()
    available = serializers.BooleanField()

    # Fields for resources with shared capacity
    capacity_total = serializers.IntegerField(required=False)
    capacity_used = serializers.IntegerField(required=False)
    capacity_remaining = serializers.IntegerField(required=False)
    free_hours = serializers.ListField(child=serializers.DictField(), required=False)
    blocking_reservations = serializers.ListField(
        child=serializers.DictField(), required=False
    )
    reason = serializers.CharField(allow_null=True, required=False)
