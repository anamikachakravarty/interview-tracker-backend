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