from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import ProjectsViewSet, ProjectCommentAPIView,DashboardAPIView


router = DefaultRouter()
router.register(r"projects", ProjectsViewSet, basename="projects")

urlpatterns = [
    path("project-comment/<str:project_id>/", ProjectCommentAPIView.as_view(), name="project-comment"),
    path("dashboard/", DashboardAPIView.as_view(), name="dashboard"),
]

urlpatterns += router.urls
