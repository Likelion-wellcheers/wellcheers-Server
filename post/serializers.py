from rest_framework import serializers
from .models import Article, Magazine, Review

class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model=Article
        fields="__all__"

class MagazineSerializer(serializers.ModelSerializer):

    class Meta:
        model=Magazine
        fields="__all__"

class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model=Review
        fields="__all__"

