from django.urls import path
from .views import (
    JobApplicationListCreateView,
    JobApplicationDetailView,
    InterviewListCreateView,
    InterviewDetailView,
    InterviewQuestionListCreateView,
    InterviewQuestionDetailView
)

urlpatterns = [
    path(
        'applications/',
        JobApplicationListCreateView.as_view(),
        name='application-list-create'
    ),

    path(
        'applications/<int:pk>/',
        JobApplicationDetailView.as_view(),
        name='application-detail'
    ),

    path(
        'applications/<int:application_id>/interviews/',
        InterviewListCreateView.as_view(),
        name='interview-list-create'
    ),

    path(
        'interviews/<int:pk>/',
        InterviewDetailView.as_view(),
        name='interview-detail'
    ),

    path(
        'interviews/<int:interview_id>/questions/',
        InterviewQuestionListCreateView.as_view(),
        name='question-list-create'
    ),
path(
        'questions/<int:pk>/',
        InterviewQuestionDetailView.as_view(),
        name='question-detail'
    ),
]
