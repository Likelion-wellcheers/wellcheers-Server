from rest_framework import serializers
from .models import Question, Answer

class QuestionSerializer(serializers.ModelSerializer):

    nickname = serializers.SerializerMethodField()
    profileimage_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Question
        fields = ['id', 'q_user_id', 'nickname', 'profileimage_url', 'region_id', 'title', 'content', 'image', 'finish', 'created_at']
    
    def get_nickname(self, obj):
        return obj.q_user_id.nickname
    
    def get_profileimage_url(self, obj):
        return obj.q_user_id.profileimage_url

class AnswerSerializer(serializers.ModelSerializer):

    q_user_nickname = serializers.SerializerMethodField()
    q_user_profileimage_url = serializers.SerializerMethodField()

    a_user_nickname = serializers.SerializerMethodField()
    a_user_profileimage_url = serializers.SerializerMethodField()

    class Meta:
        model = Answer
        fields = ['id', 'q_id', 'q_user_nickname', 'q_user_profileimage_url', 'a_user_id', 'a_user_nickname', 'a_user_profileimage_url', 'content', 'image', 'created_at']

    def get_q_user_nickname(self, obj):
        return obj.q_id.q_user_id.nickname
    
    def get_q_user_profileimage_url(self, obj):
        return obj.q_id.q_user_id.profileimage_url
    
    def get_a_user_nickname(self, obj):
        return obj.a_user_id.nickname
    
    def get_a_user_profileimage_url(self, obj):
        return obj.a_user_id.profileimage_url