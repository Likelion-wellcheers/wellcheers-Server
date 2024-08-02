from rest_framework import serializers
from .models import Article, Magazine, Review
from house.models import Region

class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model=Article
        fields="__all__"

class MagazineSerializer(serializers.ModelSerializer):

    class Meta:
        model=Magazine
        fields="__all__"

class ReviewSerializer(serializers.ModelSerializer):
    city = serializers.SerializerMethodField()
    gugoon = serializers.SerializerMethodField()

    class Meta:
        model=Review
        fields= ['id', 'user_id' , 'region_id' ,'content', 'score' , 'image', 'city' ,'gugoon' ]
    
    def city(self, obj):
        return obj.city()
    def gugoon(self, obj):
        return obj.gugoon()

    region_id = serializers.PrimaryKeyRelatedField(queryset=Region.objects.all())

