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

from accounts.models import User
from .models import Article , Magazine, Review
from .serializers import ArticleSerializer,MagazineSerializer, ReviewSerializer
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
    def get(self, request,id ):
        city_code= request.data.get(city_code=id)
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
    def get(self, request,id):
        city_code= request.data.get(city_code=id)
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

class Regionreview(APIView): # 사용자가 쓰고 , 삭제하고, 리스트로 보는 용 함수
    def post(self, request, id):
        token = request.data.get('access_token') # 엑세스 토큰으로 사용자 식별
        user = User.get_user_or_none_by_token(token=token)
        if user is None: # 해당 토큰으로 식별된 유저가 없는 경우
            return Response({"error": "User 가 없습니다. 글쓰기 불가."}, status=status.HTTP_404_NOT_FOUND)

        region = get_object_or_404(Region, city_code=id)  # 지역 정보 불러오기

        data = request.data.copy() # request를 복사해서 Review Serializer 에 추가되어야하는 body 필드를 추가한다.
        data['user_id'] = user.id
        data['region_id'] = region.id 

        serializer = ReviewSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Regionserializer=RegionSerializer(region_id=id) # 지역정보 (id 뿐만 아니라 city_code 까지)가 필요해서 불러옴.
        # serializer = ReviewSerializer(data=request.data)
        # serializer.save(user_id=user.id, city_code=Regionserializer.city_code)
        
        # return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def get(self, request, id): #해당되는 지역의 지역후기 불러오는 기능. id 가 city_code 값이다.
        city_code= request.data.get(city_code=id)

        if not city_code:# city 존재여부 확인
                return Response({"error": "해당되는 도시가 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

        region = get_object_or_404(Region, city_code=city_code) #city_code 의 region으로 region 불러옴.
        review_list= Review.objects.filter(region_id=region.id, Many=True) # FK 비교해서 리뷰 불러옴.

        return Response(review_list.data)

    def delete(self, request, id):
        token = request.data.get('access_token')  # 엑세스 토큰으로 사용자 식별
        user = User.get_user_or_none_by_token(token=token)
        if user is None:  # 해당 토큰으로 식별된 유저가 없는 경우
            return Response({"error": "User가 없습니다. 삭제 불가."}, status=status.HTTP_404_NOT_FOUND)

        review = get_object_or_404(Review, id=id, user_id=user.id)  # 리뷰 불러오기 및 사용자 확인
        review.delete()
        return Response({"success": "리뷰가 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)

class Regionreviewlook(APIView): #개별로 후기보는거 함수
     def get(self,request, id):
          
          review=get_object_or_404(Review, id=id)
          Reviewserializer=ReviewSerializer(review, many=True)
          return Response(Reviewserializer.data)
          
# Create your views here.
