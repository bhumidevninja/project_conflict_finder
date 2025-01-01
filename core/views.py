from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
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
    filterset_fields = ["status", "user"]
    search_fields = ["title", "desc", "keywords"]
    ordering_fields = ["created_at", "updated_at", "title"]
    ordering = ["created_at"]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    def list(self, request, *args, **kwargs):
        if request.user.is_superuser:
            project = Projects.objects.all()
        else:
            project = Projects.objects.filter(user=request.user)
        serializer = ProjectsSerializer(project, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        try:
            # Extract the project instance from the URL and user from request
            project = self.get_object()

            # Get the 'status' from the request data
            status_value = request.data.get("status")

            # Validate that the status is provided and is valid
            if not status_value:
                raise ValidationError("The 'status' field is required.")
            
            valid_statuses = [status[0] for status in Projects.STATUS]
            if status_value not in valid_statuses:
                raise ValidationError(f"Invalid status: '{status_value}'. Valid choices are: {valid_statuses}")

            # Update the status
            project.status = status_value
            project.save()

            # Serialize the updated project and return the response
            serializer = self.get_serializer(project)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except ValidationError as e:
            # Return validation error response
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Catch all other exceptions
            return Response(
                {"detail": "An error occurred while processing your request.", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=["post"])
    def conflict_suggestion(self, request):
        new_desc = request.data.get("desc")
        if not new_desc:
            return Response(
                {"detail": "Description is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            suggestions = get_suggestions(new_desc)
            return Response({"suggestions": suggestions}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {
                    "detail": "An error occurred while generating suggestions.",
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    