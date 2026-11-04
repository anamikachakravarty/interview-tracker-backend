
from rest_framework import status
from rest_framework.test import APITestCase

from .models import JobApplication, Interview, InterviewQuestion


class ApplicationsAPITests(APITestCase):

    def setUp(self):
        # Create a job application for tests involving interviews.
        self.application = JobApplication.objects.create(
            company_name="ABC Technologies",
            job_role="Data Analyst",
            application_date="2026-11-04",
            application_status="Applied",
            application_source="LinkedIn",
            general_notes="Test application"
        )

        # Create an interview belonging to that application.
        self.interview = Interview.objects.create(
            application=self.application,
            round_name="Technical Interview",
            interview_date="2026-11-10",
            interview_time="11:30:00",
            interview_mode="Online",
            interviewer="Technical Lead",
            interview_outcome="Scheduled"
        )

        # Create a question belonging to that interview.
        self.question = InterviewQuestion.objects.create(
            interview=self.interview,
            question_text="Explain the difference between INNER JOIN and LEFT JOIN.",
            answer_text="",
            position=1
        )

    # TEST 1: Retrieve all job applications.
    def test_get_applications(self):
        response = self.client.get("/api/applications/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    # TEST 2: Create a job application.
    def test_create_application(self):
        data = {
            "company_name": "XYZ Analytics",
            "job_role": "Junior Data Analyst",
            "application_date": "2026-11-04",
            "application_status": "Applied",
            "application_source": "Company Website"
        }

        response = self.client.post(
            "/api/applications/",
            data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(JobApplication.objects.count(), 2)

    # TEST 3: Retrieve one job application.
    def test_get_application_detail(self):
        response = self.client.get(
            f"/api/applications/{self.application.id}/"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["company_name"],
            "ABC Technologies"
        )

    # TEST 4: Update a job application's status.
    def test_update_application(self):
        response = self.client.patch(
            f"/api/applications/{self.application.id}/",
            {"application_status": "Interviewing"},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.application.refresh_from_db()
        self.assertEqual(
            self.application.application_status,
            "Interviewing"
        )

    # TEST 5: Create an interview under an application.
    def test_create_interview(self):
        data = {
            "round_name": "HR Interview",
            "interview_date": "2026-11-12",
            "interview_time": "14:00:00",
            "interview_mode": "Online",
            "interviewer": "HR Manager",
            "interview_outcome": "Scheduled"
        }

        response = self.client.post(
            f"/api/applications/{self.application.id}/interviews/",
            data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.application.interviews.count(), 2)

    # TEST 6: Retrieve interviews belonging to an application.
    def test_get_interviews(self):
        response = self.client.get(
            f"/api/applications/{self.application.id}/interviews/"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    # TEST 7: Create a question under an interview.
    def test_create_interview_question(self):
        data = {
            "question_text": "What is database normalization?",
            "answer_text": "It organizes data to reduce redundancy.",
            "position": 2
        }

        response = self.client.post(
            f"/api/interviews/{self.interview.id}/questions/",
            data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.interview.questions.count(), 2)

    # TEST 8: Update an interview question.
    def test_update_interview_question(self):
        response = self.client.patch(
            f"/api/questions/{self.question.id}/",
            {
                "answer_text": "INNER JOIN returns matching rows; LEFT JOIN preserves all left-side rows."
            },
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.question.refresh_from_db()
        self.assertIn("INNER JOIN", self.question.answer_text)

    # TEST 9: Delete an interview question.
    def test_delete_interview_question(self):
        response = self.client.delete(
            f"/api/questions/{self.question.id}/"
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(InterviewQuestion.objects.count(), 0)
