from rest_framework import serializers
from datetime import timedelta
from django.utils import timezone

from .models import (
    LearningTopic,
    LearningModule,
    LearningMilestone,
    LearningResource,
    LearningNote,
    LearningRevision
)


class LearningTopicSerializer(serializers.ModelSerializer):
    progress_percentage = serializers.ReadOnlyField()
    class Meta:
        model = LearningTopic
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class LearningModuleSerializer(serializers.ModelSerializer):
    progress_percentage = serializers.ReadOnlyField()
    class Meta:
        model = LearningModule
        fields = '__all__'
        read_only_fields = ['id', 'topic', 'created_at', 'updated_at']


class LearningMilestoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningMilestone
        fields = '__all__'
        read_only_fields = ['id', 'module', 'completed_at', 'created_at', 'updated_at']

    def update(self, instance, validated_data):
        was_completed = instance.is_completed

        instance = super().update(instance, validated_data)

        if instance.is_completed and not was_completed:
            instance.completed_at = timezone.now()
            instance.save(update_fields=['completed_at'])

            # Schedule three revisions.
            revision_intervals = [1, 3, 7]

            for number, days in enumerate(revision_intervals, start=1):
                LearningRevision.objects.get_or_create(
                    milestone=instance,
                    revision_number=number,
                    defaults={
                        'scheduled_date': (
                            timezone.localdate() + timedelta(days=days)
                        )
                    }
                )

        elif not instance.is_completed and was_completed:
            instance.completed_at = None
            instance.save(update_fields=['completed_at'])

            # Remove pending revisions, preserving completed history.
            instance.revisions.filter(status='Pending').delete()

        instance.module.topic.update_status()

        return instance

class LearningResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningResource
        fields = '__all__'
        read_only_fields = ['id', 'milestone', 'created_at', 'completed_at']

    def validate(self, attrs):
        # On PATCH, retain the existing parent if it wasn't supplied.
        topic = attrs.get('topic', getattr(self.instance, 'topic', None))
        module = attrs.get('module', getattr(self.instance, 'module', None))

        # Exactly one parent must be provided: a topic OR a module.
        if (topic is None) == (module is None):
            raise serializers.ValidationError(
                "A resource must belong to exactly one topic or module."
            )

        return attrs

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)

        if instance.status == 'Completed':
            if instance.completed_at is None:
                instance.completed_at = timezone.now()
        else:
            instance.completed_at = None

        instance.save(update_fields=['completed_at'])
        return instance

class LearningNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningNote
        fields = '__all__'
        read_only_fields = ['id', 'topic', 'created_at', 'updated_at']


class LearningRevisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningRevision
        fields = '__all__'
        read_only_fields = [
            'id',
            'milestone',
            'created_at',
            'completed_at'
        ]

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)

        if instance.status == 'Completed':
            if instance.completed_at is None:
                instance.completed_at = timezone.now()
        else:
            instance.completed_at = None

        instance.save(update_fields=['completed_at'])

        return instance    