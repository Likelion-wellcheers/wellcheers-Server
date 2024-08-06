from rest_framework import serializers
from .models import Article, Magazine, Review, MagazinePhoto
from house.models import Region
from accounts.models import User

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
    region_id = serializers.SerializerMethodField()
    city = serializers.SerializerMethodField()
    gugoon = serializers.SerializerMethodField()
    profileimage_url = serializers.SerializerMethodField()
    nickname = serializers.SerializerMethodField()

    class Meta:
        model=Review
        fields= ['id', 'user_id' , 'region_id' ,'city', 'gugoon', 'content', 'score' , 'image', 'city' ,'gugoon' , 'profileimage_url', 'nickname', 'created_at']

    def get_region_id(self, obj):
        return obj.region_id.id

    def get_city(self, obj):
        return obj.region_id.city

    def get_gugoon(self, obj):
        return obj.region_id.gugoon

    def get_profileimage_url(self, obj):
        return obj.user_id.profileimage_url if obj.user_id.profileimage_url else None

    def get_nickname(self, obj):
        return obj.user_id.nickname if obj.user_id.nickname else None

