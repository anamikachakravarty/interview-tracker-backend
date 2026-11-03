from rest_framework import serializers

from .models import JobApplication, Interview, InterviewQuestion


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


class InterviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interview
        fields = [
            'id',
            'application',
            'round_name',
            'interview_date',
            'interview_time',
            'interview_mode',
            'interviewer',
            'platform_location',
            'interview_outcome',
            'feedback',
            'personal_notes',
            'created_at',
            'updated_at',
        ]

        read_only_fields = [
            'id',
            'application',
            'created_at',
            'updated_at'
        ]


class InterviewQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewQuestion
        fields = [
            'id',
            'interview',
            'question_text',
            'answer_text',
            'position',
            'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'id',
            'interview',
            'created_at',
            'updated_at'
        ]
