
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import (
    LearningTopic,
    LearningModule,
    LearningMilestone,
    LearningResource,
    LearningNote,
    LearningRevision
)

from .serializers import (
    LearningTopicSerializer,
    LearningModuleSerializer,
    LearningMilestoneSerializer,
    LearningResourceSerializer,
    LearningNoteSerializer,
    LearningRevisionSerializer
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

class LearningNoteListCreateView(APIView):

    def get(self, request, topic_id):
        topic = get_object_or_404(LearningTopic, pk=topic_id)

        try:
            note = topic.notes
        except LearningNote.DoesNotExist:
            return Response(
                {"detail": "No notes found for this topic."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = LearningNoteSerializer(note)
        return Response(serializer.data)

    def post(self, request, topic_id):
        topic = get_object_or_404(LearningTopic, pk=topic_id)

        if LearningNote.objects.filter(topic=topic).exists():
            return Response(
                {"detail": "Notes already exist for this topic. Update them instead."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = LearningNoteSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(topic=topic)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LearningNoteDetailView(APIView):

    def get_object(self, pk):
        return get_object_or_404(LearningNote, pk=pk)

    def get(self, request, pk):
        note = self.get_object(pk)
        serializer = LearningNoteSerializer(note)
        return Response(serializer.data)

    def put(self, request, pk):
        note = self.get_object(pk)
        serializer = LearningNoteSerializer(note, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        note = self.get_object(pk)
        serializer = LearningNoteSerializer(
            note, data=request.data, partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        note = self.get_object(pk)
        note.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class LearningRevisionListCreateView(APIView):

    def get(self, request, milestone_id):
        milestone = get_object_or_404(
            LearningMilestone, pk=milestone_id
        )

        revisions = milestone.revisions.all()
        serializer = LearningRevisionSerializer(revisions, many=True)

        return Response(serializer.data)

    def post(self, request, milestone_id):
        milestone = get_object_or_404(
            LearningMilestone, pk=milestone_id
        )

        serializer = LearningRevisionSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(milestone=milestone)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LearningRevisionDetailView(APIView):

    def get_object(self, pk):
        return get_object_or_404(LearningRevision, pk=pk)

    def get(self, request, pk):
        revision = self.get_object(pk)
        serializer = LearningRevisionSerializer(revision)
        return Response(serializer.data)

    def put(self, request, pk):
        revision = self.get_object(pk)
        serializer = LearningRevisionSerializer(
            revision, data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        revision = self.get_object(pk)
        serializer = LearningRevisionSerializer(
            revision, data=request.data, partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        revision = self.get_object(pk)
        revision.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class LearningProgressSummaryView(APIView):

    def get(self, request):
        topics = LearningTopic.objects.all().order_by('-created_at')

        result = []

        for topic in topics:
            modules_data = []

            for module in topic.modules.all().order_by('position'):
                modules_data.append({
                    'id': module.id,
                    'title': module.title,
                    'weight': module.weight,
                    'progress_percentage': module.progress_percentage,
                    'milestones_total': module.milestones.count(),
                    'milestones_completed': module.milestones.filter(
                        is_completed=True
                    ).count()
                })

            result.append({
                'id': topic.id,
                'title': topic.title,
                'status': topic.status,
                'progress_percentage': topic.progress_percentage,
                'modules': modules_data
            })

        return Response(result)    