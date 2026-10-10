from unittest.mock import patch

from django.contrib.auth.models import User
from django.db import DatabaseError
from django.test import TestCase


class AuthenticationTests(TestCase):
    def test_register_creates_user_and_redirects_to_login(self):
        response = self.client.post(
            "/register/",
            {"username": "student", "password": "StrongPassword123!"},
        )

        self.assertRedirects(response, "/login/")
        self.assertTrue(User.objects.filter(username="student").exists())

    def test_login_authenticates_registered_user(self):
        User.objects.create_user(username="student", password="StrongPassword123!")

        response = self.client.post(
            "/login/",
            {"username": "student", "password": "StrongPassword123!"},
        )

        self.assertRedirects(response, "/")
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    @patch("qa.views.User.objects.filter", side_effect=DatabaseError)
    def test_register_returns_actionable_response_when_database_is_unavailable(self, _filter):
        response = self.client.post(
            "/register/",
            {"username": "student", "password": "StrongPassword123!"},
        )

        self.assertEqual(response.status_code, 503)
        self.assertContains(response, "Account service is temporarily unavailable", status_code=503)
    @patch("qa.views.authenticate", side_effect=DatabaseError)
    def test_login_returns_actionable_response_when_database_is_unavailable(self, _authenticate):
        response = self.client.post(
            "/login/",
            {"username": "student", "password": "StrongPassword123!"},
        )

        self.assertEqual(response.status_code, 503)
        self.assertContains(response, "Account service is temporarily unavailable", status_code=503)
