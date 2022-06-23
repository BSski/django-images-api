from django.test import TestCase
from django.urls import reverse


class BaseTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.home_url = reverse("images:api-root")


class CantAccessEndpointsWithoutLoginTest(BaseTest):
    def test_cant_access_homepage_endpoint_without_login(self):
        response = self.client.get(self.home_url, secure=True)
        self.assertEqual(response.status_code, 401)
