from unittest.mock import patch

from django.contrib.auth.models import User
from django.db import DatabaseError
from django.test import TestCase

from qa.groq_service import get_ai_answer, is_electrical_question


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


class QuestionScopeTests(TestCase):
    def test_rejects_non_electrical_questions_without_calling_ai(self):
        answer = get_ai_answer("Where is India?")

        self.assertIn("only electrical", answer)

    def test_accepts_electrical_terms_with_punctuation(self):
        self.assertTrue(is_electrical_question("What are motors?"))
        self.assertTrue(is_electrical_question("What is a coil?"))
        self.assertTrue(is_electrical_question("What is a cable?"))
    @patch("qa.views.authenticate", side_effect=DatabaseError)
    def test_login_returns_actionable_response_when_database_is_unavailable(self, _authenticate):
        response = self.client.post(
            "/login/",
            {"username": "student", "password": "StrongPassword123!"},
        )

        self.assertEqual(response.status_code, 503)
        self.assertContains(response, "Account service is temporarily unavailable", status_code=503)
