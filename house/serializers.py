from rest_framework import serializers
from .models import Article, Request, Review
import boto3
from django.conf import settings

class RegionSerializer(serializers.ModelSerializer):

    class Meta:
        model=Request
        fields= "__all__" #fields", exclude, readonly기능 기억

    