from rest_framework import serializers
from .models import Question, Answer

class QuestionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Question
        fields = ['q_user_id', 'region_id', 'title', 'content', 'image', 'finish']

class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = ['q_id', 'a_user_id', 'content']