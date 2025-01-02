from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import ProjectsViewSet,ProjectCommentAPIView


router = DefaultRouter()
router.register(r'projects', ProjectsViewSet, basename='projects')

urlpatterns = [
     path('project-comment/', ProjectCommentAPIView.as_view(), name='project-comment'),
]

urlpatterns += router.urls
