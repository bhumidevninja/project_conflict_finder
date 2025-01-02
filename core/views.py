from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from .models import Projects,ProjectComment
from core.utils.conflict_analyzer import get_suggestions
from .serializers import ProjectsSerializer,ProjectCommentSerializer


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
            # Extract the project instance from the URL
            project = self.get_object()

            # Check if the update is partial
            partial = kwargs.pop('partial', False)

            # Pass the project instance and request data to the serializer
            serializer = self.get_serializer(project, data=request.data, partial=partial)

            # Validate the data using the serializer
            serializer.is_valid(raise_exception=True)

            # Save the validated data
            self.perform_update(serializer)

            # Return the serialized project data
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


class ProjectCommentAPIView(APIView):
    permission_classes = [IsAdminUser]  

    def post(self, request):
        try:
            # Get the comment text from the request
            project_id = request.data.get('project')
            comment_text = request.data.get('comment')
            # Retrieve the project
            project = Projects.objects.get(id=project_id)

            if not comment_text:
                return Response(
                    {"detail": "Comment text is required."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Create the comment
            comment_instance = ProjectComment.objects.create(
                project=project,
                comment=comment_text
            )

            # Serialize and return the created comment
            serializer = ProjectCommentSerializer(comment_instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Projects.DoesNotExist:
            return Response(
                {"detail": "Project not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"detail": "An error occurred.", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )