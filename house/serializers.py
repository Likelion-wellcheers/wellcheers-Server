from rest_framework import serializers
from django.conf import settings
from .models import Infra, Mood, House_type, Region 

class InfraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Infra
        fields = ['id', 'name']

class MoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mood
        fields = ['id', 'name']

class HouseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = House_type
        fields = ['id', 'name']

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Region
        fields= "__all__"

class FilterSerializer(serializers.Serializer):
    infra = serializers.ListField(
        child=serializers.IntegerField(), required=False
    )
    mood = serializers.ListField(
        child=serializers.IntegerField(), required=False
    )
    housetype = serializers.ListField(
        child=serializers.IntegerField(), required=False
    )