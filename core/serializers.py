from rest_framework import serializers
from .models import Projects
from django.utils import timezone
from core.utils.keyword_genrator import generate_keywords
from user.serializers import UserInfoSerializer
from core.utils.conflict_analyzer import get_similarities

class ProjectsSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer(read_only=True)
    class Meta:
        model = Projects
        fields = ['title','frontend_tech','backend_tech','user','desc','status']
        read_only_fields = ['user']
    

    def validate(self, attrs):
        new_desc = attrs.get('desc')
        existing_descs = list(Projects.objects.filter(created_at__year=timezone.now().year).values_list('desc', flat=True))
        if existing_descs :
            similar_descs = get_similarities(new_desc, existing_descs)
        
            if similar_descs:
                similar_desc_info = [
                    {"desc": desc, "percentage": f"{score * 100:.2f}%"} for desc, score in similar_descs
                ]
               
                raise serializers.ValidationError({
                    "similar_descs": similar_desc_info,                    
                })
        
        return super().validate(attrs)

    def create(self, validated_data):    
        validated_data['keywords'] = generate_keywords(validated_data.get("desc"))
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)