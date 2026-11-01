from rest_framework import serializers

from .models import JobApplication


class JobApplicationSerializer(serializers.ModelSerializer):

    class Meta:
        model = JobApplication

        fields = [
            'id',
            'company_name',
            'job_role',
            'application_date',
            'job_description_url',
            'application_source',
            'application_status',
            'general_notes',
            'created_at',
            'updated_at',
        ]

        read_only_fields = [
            'id',
            'created_at',
            'updated_at',
        ]