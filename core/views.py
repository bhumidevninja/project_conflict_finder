from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Projects
from .serializers import ProjectsSerializer

class ProjectsViewSet(ModelViewSet):
    queryset = Projects.objects.all()
    serializer_class = ProjectsSerializer
    permission_classes = [IsAuthenticated]  
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_approved', 'category', 'user_id'] 
    search_fields = ['title', 'desc', 'keywords'] 
    ordering_fields = ['created_at', 'updated_at', 'title']  
    ordering = ['created_at']