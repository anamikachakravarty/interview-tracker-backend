from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import JobApplication
from .serializers import JobApplicationSerializer
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
    