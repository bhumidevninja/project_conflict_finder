from rest_framework import serializers
from .models import Projects
from core.utils.keyword_genrator import generate_keywords

class ProjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = ['title','desc','user_id','category']
    

    def create(self, validated_data):
        print("in create method", validated_data)
        validated_data['keywords'] = generate_keywords(validated_data.get("desc"))
        return super().create(validated_data)