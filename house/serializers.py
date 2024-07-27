from rest_framework import serializers
from django.conf import settings
from .models import Infra, Hobby, Lifestyle, Region ,Center, CenterReview

class InfraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Infra
        fields = ['id', 'name']

class MoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hobby
        fields = ['id', 'name']

class HouseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lifestyle
        fields = ['id', 'name']

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Region
        fields= "__all__"

class CenterSerializer(serializers.ModelSerializer):
    class Meta:
        model=Center
        fields="__all__"

class FilterSerializer(serializers.Serializer):
    infra = serializers.ListField(
        child=serializers.IntegerField(), required=False
    )
    hobby = serializers.ListField(
        child=serializers.IntegerField(), required=False
    )
    lifestyle = serializers.ListField(
        child=serializers.IntegerField(), required=False
    )