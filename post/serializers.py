from rest_framework import serializers
from .models import Article, Magazine

class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model=Article
        fields="__all__"

class MagazineSerializer(serializers.ModelSerializer):

    class Meta:
        model=Magazine
        fields="__all__"
