from django.db import models


class JobApplication(models.Model):

    class ApplicationStatus(models.TextChoices):
        APPLIED = 'Applied', 'Applied'
        ASSESSMENT = 'Assessment', 'Assessment'
        INTERVIEWING = 'Interviewing', 'Interviewing'
        OFFER_RECEIVED = 'Offer Received', 'Offer Received'
        REJECTED = 'Rejected', 'Rejected'
        WITHDRAWN = 'Withdrawn', 'Withdrawn'
        ON_HOLD = 'On Hold', 'On Hold'

    company_name = models.CharField(max_length=150)

    job_role = models.CharField(max_length=150)

    application_date = models.DateField()

    job_description_url = models.URLField(blank=True)

    application_source = models.CharField(
        max_length=100,
        blank=True
    )

    application_status = models.CharField(
        max_length=30,
        choices=ApplicationStatus.choices,
        default=ApplicationStatus.APPLIED
    )

    general_notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.company_name} - {self.job_role}"

class Interview(models.Model):

    class InterviewOutcome(models.TextChoices):
        SCHEDULED = 'Scheduled', 'Scheduled'
        AWAITING_RESULT = 'Awaiting Result', 'Awaiting Result'
        PASSED = 'Passed', 'Passed'
        FAILED = 'Failed', 'Failed'
        CANCELLED = 'Cancelled', 'Cancelled'

    class InterviewMode(models.TextChoices):
        ONLINE = 'Online', 'Online'
        IN_PERSON = 'In-person', 'In-person'
        PHONE = 'Phone', 'Phone'

    application = models.ForeignKey(
        JobApplication,
        on_delete=models.CASCADE,
        related_name='interviews'
    )

    round_name = models.CharField(max_length=100)

    interview_date = models.DateField()

    interview_time = models.TimeField(blank=True, null=True)

    interview_mode = models.CharField(
        max_length=30,
        choices=InterviewMode.choices,
        blank=True
    )

    interviewer = models.CharField(max_length=150, blank=True)

    platform_location = models.TextField(blank=True)

    interview_outcome = models.CharField(
        max_length=30,
        choices=InterviewOutcome.choices,
        default=InterviewOutcome.SCHEDULED
    )

    feedback = models.TextField(blank=True)

    personal_notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.application.company_name} - {self.round_name}"

class InterviewQuestion(models.Model):

    interview = models.ForeignKey(
        Interview,
        on_delete=models.CASCADE,
        related_name='questions'
    )

    question_text = models.TextField()

    answer_text = models.TextField(blank=True)

    position = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question_text[:80]

