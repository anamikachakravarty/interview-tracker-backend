from rest_framework import serializers

from .models import (
    LearningTopic,
    LearningModule,
    LearningMilestone,
    LearningResource
)


class LearningTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningTopic
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class LearningModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningModule
        fields = '__all__'
        read_only_fields = ['id', 'topic', 'created_at', 'updated_at']


class LearningMilestoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningMilestone
        fields = '__all__'
        read_only_fields = ['id', 'module', 'created_at', 'updated_at']


class LearningResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningResource
        fields = '__all__'
        read_only_fields = ['id', 'created_at']

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