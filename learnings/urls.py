
from django.urls import path

from .views import (
    LearningTopicListCreateView,
    LearningTopicDetailView,
    LearningModuleListCreateView,
    LearningModuleDetailView,
    LearningMilestoneListCreateView,
    LearningMilestoneDetailView,
    LearningResourceListCreateView,
    LearningResourceDetailView
)

urlpatterns = [
    # Topics
    path(
        'topics/',
        LearningTopicListCreateView.as_view(),
        name='topic-list-create'
    ),
    path(
        'topics/<int:pk>/',
        LearningTopicDetailView.as_view(),
        name='topic-detail'
    ),

    # Modules
    path(
        'topics/<int:topic_id>/modules/',
        LearningModuleListCreateView.as_view(),
        name='module-list-create'
    ),
    path(
        'modules/<int:pk>/',
        LearningModuleDetailView.as_view(),
        name='module-detail'
    ),

    # Milestones
    path(
        'modules/<int:module_id>/milestones/',
        LearningMilestoneListCreateView.as_view(),
        name='milestone-list-create'
    ),
    path(
        'milestones/<int:pk>/',
        LearningMilestoneDetailView.as_view(),
        name='milestone-detail'
    ),

    # Resources
    path(
        'resources/',
        LearningResourceListCreateView.as_view(),
        name='resource-list-create'
    ),
    path(
        'resources/<int:pk>/',
        LearningResourceDetailView.as_view(),
        name='resource-detail'
    ),
]
