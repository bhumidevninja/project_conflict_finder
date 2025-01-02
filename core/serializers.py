from rest_framework import serializers
from .models import Projects,ProjectComment
from django.utils import timezone
from core.utils.keyword_genrator import generate_keywords
from user.serializers import UserInfoSerializer
from core.utils.conflict_analyzer import get_similarities

class ProjectsSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer(read_only=True)
    class Meta:
        model = Projects
        fields = ['id','title','frontend_tech','backend_tech','user','desc','status']
        read_only_fields = ['user']
    
    def validate_status(self, value):
        """Validate the status field."""
        valid_statuses = [status[0] for status in Projects.STATUS]
        if value not in valid_statuses:
            raise serializers.ValidationError(
                f"Invalid status: '{value}'. Valid choices are: {valid_statuses}"
            )
        return value
    
    def validate_title(self, value):
        """Validate the title for uniqueness."""
        # Exclude the current project during updates
        project_id = self.instance.id if self.instance else None
        if Projects.objects.filter(title=value).exclude(id=project_id).exists():
            raise serializers.ValidationError(
                f"A project with the title '{value}' already exists."
            )
        return value


    def validate_desc(self, value):
        """Validate 'desc' for similarity with existing descriptions."""
        # Fetch all descriptions from the current year
        existing_descs = list(
            Projects.objects.filter(created_at__year=timezone.now().year)
            .exclude(id=self.instance.id if self.instance else None)  
            .values_list('desc', flat=True)
        )

        if existing_descs:
            similar_descs = get_similarities(value, existing_descs)
            if similar_descs:
                similar_desc_info = [
                    {"desc": desc, "percentage": f"{score * 100:.2f}%"} for desc, score in similar_descs
                ]
                raise serializers.ValidationError({
                    "similar_descs": similar_desc_info
                })
        return value


    def validate(self, attrs):
        # handle object level validation here.
        return super().validate(attrs)

    def create(self, validated_data):    
        validated_data['keywords'] = generate_keywords(validated_data.get("desc"))
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class ProjectCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectComment
        fields = ['id', 'comment','project', 'created_at', 'updated_at']

