from datetime import date
from decimal import Decimal

from rest_framework import status
from rest_framework.test import APITestCase

from .models import (
    LearningTopic,
    LearningModule,
    LearningMilestone,
    LearningNote,
    LearningRevision,
)


class LearningAPITests(APITestCase):

    def setUp(self):
        # Create a topic for our tests.
        self.topic = LearningTopic.objects.create(
            title="SQL Advanced Concepts",
            description="Advanced SQL interview preparation.",
            category="Database",
            priority="High",
            status="New",
        )

        # Create a module belonging to the topic.
        self.module = LearningModule.objects.create(
            topic=self.topic,
            title="Advanced SQL Joins",
            description="Learn complex joins.",
            weight=Decimal("100.00"),
            position=1,
        )

        # Create two milestones belonging to the module.
        self.milestone1 = LearningMilestone.objects.create(
            module=self.module,
            title="Understand INNER JOIN",
            weight=Decimal("50.00"),
            is_completed=False,
            position=1,
        )

        self.milestone2 = LearningMilestone.objects.create(
            module=self.module,
            title="Understand Anti JOIN",
            weight=Decimal("50.00"),
            is_completed=False,
            position=2,
        )

    # TEST 1: Retrieve topics

    def test_get_topics(self):
        response = self.client.get("/api/learning/topics/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    # TEST 2: Create a topic

    def test_create_topic(self):
        data = {
            "title": "Python Advanced",
            "description": "Advanced Python concepts.",
            "category": "Programming",
            "priority": "Medium",
            "status": "New",
        }

        response = self.client.post(
            "/api/learning/topics/",
            data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(LearningTopic.objects.count(), 2)

    # TEST 3: Retrieve modules belonging to a topic

    def test_get_modules(self):
        url = f"/api/learning/topics/{self.topic.id}/modules/"

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    # TEST 4: Create a milestone

    def test_create_milestone(self):
        url = f"/api/learning/modules/{self.module.id}/milestones/"

        data = {
            "title": "Practise LEFT JOIN",
            "description": "Write LEFT JOIN queries.",
            "weight": "25.00",
            "is_completed": False,
            "position": 3,
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.module.milestones.count(), 3)

    # TEST 5: Prevent duplicate notes

    def test_prevent_duplicate_notes(self):
        url = f"/api/learning/topics/{self.topic.id}/notes/"

        first_response = self.client.post(
            url,
            {"content": "My SQL notes."},
            format="json",
        )

        second_response = self.client.post(
            url,
            {"content": "Duplicate notes."},
            format="json",
        )

        self.assertEqual(
            first_response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            second_response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertEqual(LearningNote.objects.count(), 1)

    # TEST 6: Automatically schedule revisions on completion

    def test_milestone_completion_schedules_revisions(self):
        url = f"/api/learning/milestones/{self.milestone1.id}/"

        response = self.client.patch(
            url,
            {"is_completed": True},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.milestone1.refresh_from_db()

        self.assertTrue(self.milestone1.is_completed)
        self.assertIsNotNone(self.milestone1.completed_at)

        self.assertEqual(
            self.milestone1.revisions.count(),
            3,
        )

    # TEST 7: Revision completion timestamp

    def test_revision_completion_timestamp(self):
        revision = LearningRevision.objects.create(
            milestone=self.milestone1,
            scheduled_date=date(2026, 11, 5),
            revision_number=1,
        )

        url = f"/api/learning/revisions/{revision.id}/"

        response = self.client.patch(
            url,
            {"status": "Completed"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        revision.refresh_from_db()

        self.assertEqual(revision.status, "Completed")
        self.assertIsNotNone(revision.completed_at)

    # TEST 8: Progress summary

    def test_progress_summary(self):
        self.client.patch(
            f"/api/learning/milestones/{self.milestone1.id}/",
            {"is_completed": True},
            format="json",
        )

        response = self.client.get("/api/learning/progress/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        topic_data = response.data[0]

        self.assertEqual(
            Decimal(str(topic_data["progress_percentage"])),
            Decimal("50.00"),
        )

        self.assertEqual(topic_data["status"], "In Progress")