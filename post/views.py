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

from .models import Article
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
            return Response({"error": "시또는 도를 선택해주세요."}, status=status.HTTP_400_BAD_REQUEST)

        gugoon = Region.objects.filter(city=city).values_list('gugoon', flat=True).distinct()
        #goon = Region.objects.filter(city=city).values_list('goon', flat=True).distinct()

        if not gugoon:
            return Response({"error": "선택한 시 안에 구 또는 군이 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        return Response({
            "city": city,
            "gugoon": list(gugoon),
            #"goon": list(goon)
        }, status=status.HTTP_200_OK)
    
class ArticlesByRegionView(APIView):
    def post(self, request):
        city = request.data.get('city')
        gugoon = request.data.get('gugoon')
        #goon = request.data.get('goon')

        if not city :
            if not gugoon:
                return Response({"error": "시와 군,구를 모두 선택해주세요."}, status=status.HTTP_400_BAD_REQUEST)

        region = get_object_or_404(Region, city=city, gugoon=gugoon)

        articles = Article.objects.filter(region_id=region.id)
        article_serializer = ArticleSerializer(articles, many=True)

        if not article_serializer.data:
            return Response({"message": "해당 지역에 기사 정보가 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        return Response(article_serializer.data, status=status.HTTP_200_OK)

class MagazineByRegionView(APIView):
    def post(self, request):
        city = request.data.get('city')
        gugoon = request.data.get('gugoon')
        #goon = request.data.get('goon')

        if not city :
            if not gugoon:
                return Response({"error": "시와 군,구를 모두 선택해주세요."}, status=status.HTTP_400_BAD_REQUEST)

        region = get_object_or_404(Region, city=city, gugoon=gugoon)

        magazines = Article.objects.filter(region_id=region.id)
        magazine_serializer = MagazineSerializer(magazines, many=True)

        if not magazine_serializer.data:
            return Response({"message": "해당 지역에 기사 정보가 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        return Response(magazine_serializer.data, status=status.HTTP_200_OK)
# Create your views here.