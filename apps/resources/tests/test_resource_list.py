from django.urls import reverse
from rest_framework.test import APITestCase
from .conftest import ResourceTestSetup


class ResourceListAPITest(ResourceTestSetup, APITestCase):
    """Tests for the ResourceListView API endpoint."""

    def test_resource_list(self):
        response = self.client.get("/api/resources/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 3)
        types = {r["type"] for r in data}
        self.assertSetEqual(types, {"meeting_room", "vehicle", "equipment"})
        for r in data:
            self.assertIn("name", r)
            self.assertIn("attributes", r)
            self.assertIn("image_url", r)
