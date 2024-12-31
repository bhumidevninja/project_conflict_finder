from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from .models import Projects
from core.utils.conflict_analyzer import get_suggestions
from .serializers import ProjectsSerializer


class ProjectsViewSet(ModelViewSet):
    queryset = Projects.objects.all()
    serializer_class = ProjectsSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["status", "user_id"]
    search_fields = ["title", "desc", "keywords"]
    ordering_fields = ["created_at", "updated_at", "title"]
    ordering = ["created_at"]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request 
        return context

    @action(detail=False, methods=["post"])
    def conflict_suggestion(self, request):
        new_desc = request.data.get("desc")
        if not new_desc:
            return Response({"detail": "Description is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            suggestions = get_suggestions(new_desc)
            return Response({"suggestions": suggestions}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"detail": "An error occurred while generating suggestions.", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
