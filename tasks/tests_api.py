from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from datetime import date, timedelta


class AnalyzeAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_analyze_valid(self):
        """API should return 200 and sorted results for valid input."""
        payload = [
            {
                "title": "Task A",
                "due_date": str(date.today() + timedelta(days=3)),
                "importance": 7,
                "estimated_hours": 3,
                "dependencies": []
            },
            {
                "title": "Task B",
                "due_date": str(date.today() + timedelta(days=1)),
                "importance": 5,
                "estimated_hours": 1,
                "dependencies": []
            }
        ]

        response = self.client.post("/api/analyze/", payload, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertIn("results", response.data)

        # Sorted: Task B should be first because it's more urgent
        self.assertEqual(response.data["results"][0]["title"], "Task B")


    def test_analyze_invalid(self):
        """Invalid input should return 400."""
        payload = [
            {"title": "", "importance": 12}  # invalid
        ]

        response = self.client.post("/api/analyze/", payload, format="json")
        self.assertEqual(response.status_code, 400)


class SuggestAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_suggest_top_tasks(self):
        """Should return top 3 suggestions."""
        payload = [
            {
                "title": "Urgent Task",
                "due_date": str(date.today() + timedelta(days=1)),
                "importance": 9,
                "estimated_hours": 1,
                "dependencies": []
            },
            {
                "title": "Future Task",
                "due_date": str(date.today() + timedelta(days=30)),
                "importance": 5,
                "estimated_hours": 3,
                "dependencies": []
            }
        ]

        response = self.client.post("/api/suggest/", payload, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertIn("suggestions", response.data)

        # Should return only up to 3 items
        self.assertTrue(len(response.data["suggestions"]) <= 3)

        # Most urgent should be first
        self.assertEqual(response.data["suggestions"][0]["title"], "Urgent Task")
