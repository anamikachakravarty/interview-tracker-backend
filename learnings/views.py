
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import (
    LearningTopic,
    LearningModule,
    LearningMilestone,
    LearningResource
)

from .serializers import (
    LearningTopicSerializer,
    LearningModuleSerializer,
    LearningMilestoneSerializer,
    LearningResourceSerializer
)


# --------------------------------
# 1. LEARNING TOPIC
# --------------------------------

class LearningTopicListCreateView(APIView):

    def get(self, request):
        topics = LearningTopic.objects.all().order_by('-created_at')
        serializer = LearningTopicSerializer(topics, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = LearningTopicSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class LearningTopicDetailView(APIView):

    def get(self, request, pk):
        topic = get_object_or_404(LearningTopic, pk=pk)
        serializer = LearningTopicSerializer(topic)
        return Response(serializer.data)

    def put(self, request, pk):
        topic = get_object_or_404(LearningTopic, pk=pk)
        serializer = LearningTopicSerializer(
            topic, data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def patch(self, request, pk):
        topic = get_object_or_404(LearningTopic, pk=pk)
        serializer = LearningTopicSerializer(
            topic, data=request.data, partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        topic = get_object_or_404(LearningTopic, pk=pk)
        topic.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# --------------------------------
# 2. LEARNING MODULE
# --------------------------------

class LearningModuleListCreateView(APIView):

    def get(self, request, topic_id):
        topic = get_object_or_404(LearningTopic, pk=topic_id)

        modules = LearningModule.objects.filter(
            topic=topic
        ).order_by('position', 'created_at')

        serializer = LearningModuleSerializer(modules, many=True)
        return Response(serializer.data)

    def post(self, request, topic_id):
        topic = get_object_or_404(LearningTopic, pk=topic_id)

        serializer = LearningModuleSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(topic=topic)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class LearningModuleDetailView(APIView):

    def get(self, request, pk):
        module = get_object_or_404(LearningModule, pk=pk)
        serializer = LearningModuleSerializer(module)
        return Response(serializer.data)

    def put(self, request, pk):
        module = get_object_or_404(LearningModule, pk=pk)
        serializer = LearningModuleSerializer(
            module, data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def patch(self, request, pk):
        module = get_object_or_404(LearningModule, pk=pk)
        serializer = LearningModuleSerializer(
            module, data=request.data, partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        module = get_object_or_404(LearningModule, pk=pk)
        module.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# --------------------------------
# 3. LEARNING MILESTONE
# --------------------------------

class LearningMilestoneListCreateView(APIView):

    def get(self, request, module_id):
        module = get_object_or_404(LearningModule, pk=module_id)

        milestones = LearningMilestone.objects.filter(
            module=module
        ).order_by('position', 'created_at')

        serializer = LearningMilestoneSerializer(
            milestones, many=True
        )
        return Response(serializer.data)

    def post(self, request, module_id):
        module = get_object_or_404(LearningModule, pk=module_id)

        serializer = LearningMilestoneSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(module=module)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class LearningMilestoneDetailView(APIView):

    def get(self, request, pk):
        milestone = get_object_or_404(LearningMilestone, pk=pk)
        serializer = LearningMilestoneSerializer(milestone)
        return Response(serializer.data)

    def put(self, request, pk):
        milestone = get_object_or_404(LearningMilestone, pk=pk)
        serializer = LearningMilestoneSerializer(
            milestone, data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def patch(self, request, pk):
        milestone = get_object_or_404(LearningMilestone, pk=pk)
        serializer = LearningMilestoneSerializer(
            milestone, data=request.data, partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        milestone = get_object_or_404(LearningMilestone, pk=pk)
        milestone.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# --------------------------------
# 4. LEARNING RESOURCE
# --------------------------------

class LearningResourceListCreateView(APIView):

    def get(self, request):
        resources = LearningResource.objects.all().order_by('-created_at')

        serializer = LearningResourceSerializer(
            resources, many=True
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = LearningResourceSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class LearningResourceDetailView(APIView):

    def get(self, request, pk):
        resource = get_object_or_404(LearningResource, pk=pk)
        serializer = LearningResourceSerializer(resource)
        return Response(serializer.data)

    def put(self, request, pk):
        resource = get_object_or_404(LearningResource, pk=pk)
        serializer = LearningResourceSerializer(
            resource, data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def patch(self, request, pk):
        resource = get_object_or_404(LearningResource, pk=pk)
        serializer = LearningResourceSerializer(
            resource, data=request.data, partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        resource = get_object_or_404(LearningResource, pk=pk)
        resource.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
