from rest_framework import serializers
from .models import Question

class QuestionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Question
        fields = ['q_user_id', 'region_id', 'title', 'content', 'image', 'finish']