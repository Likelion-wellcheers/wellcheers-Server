from rest_framework import serializers
from django.conf import settings
from .models import Infra, Hobby, Lifestyle, Region ,Center, CenterReview, Cart, Report

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

class CartSerializer(serializers.ModelSerializer):
    center1 = CenterSerializer()
    center2 = CenterSerializer()
    center3 = CenterSerializer()

    class Meta:
        model = Cart
        fields = ['id', 'center1', 'center2', 'center3', 'total_cost']

class CartcostSerializer(serializers.ModelSerializer):
    total_cost = serializers.DecimalField(max_digits=10, decimal_places=2) #소숫점 포함 10자리
    class Meta:
        model=Cart
        fields= ['total_cost']

class FilterSerializer(serializers.Serializer):
    # 각 필드를 정수 리스트로 선언
    infra = serializers.ListField(
        child=serializers.IntegerField(), required=False
    )
    hobby = serializers.ListField(
        child=serializers.IntegerField(), required=False
    )
    lifestyle = serializers.ListField(
        child=serializers.IntegerField(), required=False
    )

class CenterReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = CenterReview
        fields = ['center_id', 'user_id', 'content']