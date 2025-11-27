from django.test import TestCase
from datetime import date, timedelta

from tasks.scoring import calculate_task_score
from tasks.dependency_checker import detect_cycle


class ScoringTests(TestCase):

    def test_urgency_increases_score(self):
        """Task due tomorrow should score higher than task due in 20 days."""
        t1 = {"title": "A", "due_date": date.today() + timedelta(days=1),
              "importance": 5, "estimated_hours": 2, "dependencies": []}

        t2 = {"title": "B", "due_date": date.today() + timedelta(days=20),
              "importance": 5, "estimated_hours": 2, "dependencies": []}

        score1 = calculate_task_score(t1)
        score2 = calculate_task_score(t2)

        self.assertTrue(score1 > score2)


    def test_importance_affects_score(self):
        """Higher importance should give higher score."""
        t1 = {"title": "A", "due_date": None,
              "importance": 10, "estimated_hours": 2, "dependencies": []}

        t2 = {"title": "B", "due_date": None,
              "importance": 3, "estimated_hours": 2, "dependencies": []}

        self.assertTrue(calculate_task_score(t1) > calculate_task_score(t2))


    def test_low_effort_increases_score(self):
        """Less estimated hours = higher score."""
        t1 = {"title": "A", "due_date": None,
              "importance": 5, "estimated_hours": 1, "dependencies": []}

        t2 = {"title": "B", "due_date": None,
              "importance": 5, "estimated_hours": 9, "dependencies": []}

        self.assertTrue(calculate_task_score(t1) > calculate_task_score(t2))


class CircularDependencyTests(TestCase):

    def test_detects_cycle(self):
        """A -> B -> A should be detected."""
        tasks = [
            {"title": "A", "dependencies": ["B"]},
            {"title": "B", "dependencies": ["A"]},
        ]
        self.assertIsNotNone(detect_cycle(tasks))

    def test_no_cycle(self):
        """A -> B (no cycle)."""
        tasks = [
            {"title": "A", "dependencies": ["B"]},
            {"title": "B", "dependencies": []},
        ]
        self.assertIsNone(detect_cycle(tasks))
