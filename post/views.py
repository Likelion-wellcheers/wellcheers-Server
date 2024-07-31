from django.shortcuts import render
from django.http import JsonResponse # 추가 
from django.shortcuts import get_object_or_404 # 추가
from django.views.decorators.http import require_http_methods
import json
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.views import status
from rest_framework import status
from django.http import Http404

from .models import Article , Magazine
from .serializers import ArticleSerializer,MagazineSerializer
from house.models import Region
from house.serializers import RegionSerializer

class AtriclePost(APIView):
        def get(self, request, format=None):
            articles=Article.objects.all()
            serializers=ArticleSerializer(articles, many=True)
            return Response(serializers.data)
        
class ChoiceRegion(APIView):
    def post(self, request):
        city = request.data.get('city')
        if not city:
            return Response({"error": "시 또는 도를 선택해주세요."}, status=status.HTTP_400_BAD_REQUEST)

        choice_regions = Region.objects.filter(city=city) #해당 city 를 갖고있는 지역 개체들 불러오기
        gugoon = Region.objects.filter(city=city).values_list('gugoon', flat=True).distinct()
        #goon = Region.objects.filter(city=city).values_list('goon', flat=True).distinct() 모델수정전

        region_data = list(choice_regions.values()) #여러개일테니까 데이터값을 리스트로 불러옴.
        if not gugoon:
            return Response({"error": "시만 존재하는 도시입니다",
                             "city":city,
                             "region_data": region_data.city_code})
        return Response({
            "city":city,
            "gugoon": list(gugoon),
            #"goon": list(goon),
            "city_code": region_data.city_code # 걸러진 region 의 city_code 값과 해당되는 구군 이름도 따로 보내줌.
        }, status=status.HTTP_200_OK)
    
class WellfareByRegionView(APIView):
    def post(self, request):
        city_code= request.data.get('city_code')
        #goon = request.data.get('goon')

        if not city_code :
            return Response({"error": "해당되는 도시가 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

        region = get_object_or_404(Region, city_code=city_code)

        articles = Article.objects.filter(region_id=region.id)
        article_serializer = MagazineSerializer(articles, many=True)

        if not article_serializer.data:
            return Response({"message": "해당 지역에 복지정책 정보가 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        return Response(article_serializer.data, status=status.HTTP_200_OK)

class MagazineByRegionView(APIView):
    def post(self, request):
        city_code= request.data.get('city_code')
        # city = request.data.get('city')
        # gugoon = request.data.get('gugoon')
        #goon = request.data.get('goon')

        if not city_code:
                return Response({"error": "해당되는 도시가 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

        region = get_object_or_404(Region, city_code=city_code)

        magazines = Magazine.objects.filter(region_id=region.id)
        magazine_serializer = ArticleSerializer(magazines, many=True)

        if not magazine_serializer.data:
            return Response({"message": "해당 지역에 매거진 정보가 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        return Response(magazine_serializer.data, status=status.HTTP_200_OK)
# Create your views here.