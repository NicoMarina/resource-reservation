from rest_framework import serializers


class ResourceSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    description = serializers.CharField(allow_blank=True, allow_null=True)
    type = serializers.CharField(source="get_type")
    attributes = serializers.JSONField(source="get_attributes")
    image_url = serializers.CharField(allow_blank=True, allow_null=True)
