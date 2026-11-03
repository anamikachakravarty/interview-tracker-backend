from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import JobApplication, Interview, InterviewQuestion
from .serializers import JobApplicationSerializer, InterviewSerializer, InterviewQuestionSerializer
from django.shortcuts import get_object_or_404


class JobApplicationListCreateView(APIView):

    def get(self, request):

        applications = JobApplication.objects.all().order_by('-created_at')

        serializer = JobApplicationSerializer(
            applications,
            many=True
        )

        return Response(serializer.data)


    def post(self, request):

        serializer = JobApplicationSerializer(data=request.data)

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

class JobApplicationDetailView(APIView):

    def get(self, request, pk):

        application = get_object_or_404(
            JobApplication,
            pk=pk
        )

        serializer = JobApplicationSerializer(application)

        return Response(serializer.data)


    def put(self, request, pk):

        application = get_object_or_404(
            JobApplication,
            pk=pk
        )

        serializer = JobApplicationSerializer(
            application,
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


    def patch(self, request, pk):

        application = get_object_or_404(
            JobApplication,
            pk=pk
        )

        serializer = JobApplicationSerializer(
            application,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


    def delete(self, request, pk):

        application = get_object_or_404(
            JobApplication,
            pk=pk
        )

        application.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )


class InterviewListCreateView(APIView):

    def get(self, request, application_id):
        application = get_object_or_404(
            JobApplication,
            pk=application_id
        )

        interviews = Interview.objects.filter(
            application=application
        ).order_by('interview_date', 'interview_time')

        serializer = InterviewSerializer(interviews, many=True)

        return Response(serializer.data)

    def post(self, request, application_id):
        application = get_object_or_404(
            JobApplication,
            pk=application_id
        )

        serializer = InterviewSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(application=application)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class InterviewDetailView(APIView):

    def get(self, request, pk):
        interview = get_object_or_404(Interview, pk=pk)
        serializer = InterviewSerializer(interview)
        return Response(serializer.data)

    def put(self, request, pk):
        interview = get_object_or_404(Interview, pk=pk)
        serializer = InterviewSerializer(interview, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def patch(self, request, pk):
        interview = get_object_or_404(Interview, pk=pk)
        serializer = InterviewSerializer(
            interview,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        interview = get_object_or_404(Interview, pk=pk)
        interview.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class InterviewQuestionListCreateView(APIView):

    def get(self, request, interview_id):
        interview = get_object_or_404(Interview, pk=interview_id)
        questions = InterviewQuestion.objects.filter(
            interview=interview
        ).order_by('position', 'created_at')

        serializer = InterviewQuestionSerializer(questions, many=True)
        return Response(serializer.data)

    def post(self, request, interview_id):
        interview = get_object_or_404(Interview, pk=interview_id)
        serializer = InterviewQuestionSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(interview=interview)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class InterviewQuestionDetailView(APIView):

    def get(self, request, pk):
        question = get_object_or_404(InterviewQuestion, pk=pk)
        serializer = InterviewQuestionSerializer(question)
        return Response(serializer.data)

    def put(self, request, pk):
        question = get_object_or_404(InterviewQuestion, pk=pk)
        serializer = InterviewQuestionSerializer(
            question, data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def patch(self, request, pk):
        question = get_object_or_404(InterviewQuestion, pk=pk)
        serializer = InterviewQuestionSerializer(
            question, data=request.data, partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        question = get_object_or_404(InterviewQuestion, pk=pk)
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
