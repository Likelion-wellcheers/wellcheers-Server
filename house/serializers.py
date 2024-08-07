from rest_framework import serializers
from django.conf import settings
from .models import Infra, Hobby, Lifestyle, Region ,Center, CenterReview, Cart, Report, CenterPhoto

class InfraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Infra
        fields = ['id', 'name']

class HobbySerializer(serializers.ModelSerializer):
    class Meta:
        model = Hobby
        fields = ['id', 'name']

class LifestyleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lifestyle
        fields = ['id', 'name']

class RegionSerializer(serializers.ModelSerializer):

    lifename = serializers.SerializerMethodField()
    hobbyname = serializers.SerializerMethodField()
    infraname = serializers.SerializerMethodField()

    class Meta:
        model=Region
        fields = [
            'id', 'lstyle_id', 'infra_id', 'hobby_id', 'city_code', 'city', 'gugoon',
            'longtitude', 'latitude', 'thumbnail', 'lifename', 'hobbyname', 'infraname'
        ]
        #fields=[ 'id', 'lstyle_id', 'infra_id', 'hobby_id', 'city_code','city', 'gugoon', 'longtitude', 'latitude', 'thumbnail']
    def get_lifename(self, obj):
        return [lifestyle.name for lifestyle in obj.lstyle_id.all()]

    def get_hobbyname(self, obj):
        return [hobby.name for hobby in obj.hobby_id.all()]

    def get_infraname(self, obj):
        return [infra.name for infra in obj.infra_id.all()]

class MagPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model=CenterPhoto
        fields = ['image']

class CenterSerializer(serializers.ModelSerializer):
    photos = MagPhotoSerializer(many=True, read_only=True)
    city = serializers.SerializerMethodField()
    gugoon = serializers.SerializerMethodField()

    class Meta:
        model = Center
        fields = ['id', 'name', 'region_id', 'address', 'time', 'cost', 'longtitude', 'latitude', 'thumbnail', 'city','gugoon', 'phonenum', 'photos']

    def city(self, obj):
        return obj.city()
    def gugoon(self, obj):
        return obj.gugoon()

    region_id = serializers.PrimaryKeyRelatedField(queryset=Region.objects.all())
    # class Meta:
    #     model=Center
    #     fields="__all__"

class CartSerializer(serializers.ModelSerializer):

    center1 = CenterSerializer(allow_null=True, required = False)
    center2 = CenterSerializer(allow_null=True, required = False)
    center3 = CenterSerializer(allow_null=True, required = False)
    center4 = CenterSerializer(allow_null=True, required = False)
    center5 = CenterSerializer(allow_null=True, required = False)

    class Meta:
        model = Cart
        fields = ['id', 'center1', 'center2', 'center3', 'center4', 'center5', 'total_cost']

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
    name = serializers.SerializerMethodField()
    region_id = serializers.SerializerMethodField()
    city = serializers.SerializerMethodField()
    gugoon = serializers.SerializerMethodField()
    profileimage_url = serializers.SerializerMethodField()
    nickname = serializers.SerializerMethodField()

    class Meta:
        model = CenterReview
        fields = ['id', 'center_id', 'name', 'user_id','region_id', 'city', 'gugoon', 'content','created_at','profileimage_url','nickname','score', 'thumbnail']

    def get_name(self, obj):
        return obj.center_id.name
    
    def get_region_id(self, obj):
        return obj.center_id.region_id.id

    def get_city(self, obj):
        return obj.center_id.region_id.city

    def get_gugoon(self, obj):
        return obj.center_id.region_id.gugoon

    def get_profileimage_url(self, obj):
        return obj.user_id.profileimage_url if obj.user_id.profileimage_url else None

    def get_nickname(self, obj):
        return obj.user_id.nickname if obj.user_id.nickname else None

class ReportSerializer(serializers.ModelSerializer):

    city = serializers.SerializerMethodField()
    gugoon = serializers.SerializerMethodField()

    class Meta:
        model = Report
        fields = ['user_id', 'region_id', 'plan1', 'plan2', 'plan3', 'city', 'gugoon', 'created_at']

    def city(self, obj):
        return obj.city()
    def gugoon(self, obj):
        return obj.gugoon()

    region_id = serializers.PrimaryKeyRelatedField(queryset=Region.objects.all())