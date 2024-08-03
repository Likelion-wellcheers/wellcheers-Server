from rest_framework import serializers
from .models import Article, Magazine, Review, MagazinePhoto
from house.models import Region

class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model=Article
        fields="__all__"

class MagazineSerializer(serializers.ModelSerializer):

    class Meta:
        model=Magazine
        fields="__all__"

class MagPhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model=MagazinePhoto
        fields = ['image']

class MagOneSerializer(serializers.ModelSerializer):
    photos = MagPhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Magazine
        fields =['id', 'content', 'image','region_id','created_at','photos']

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

