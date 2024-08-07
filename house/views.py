import random
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

from accounts.views import ReturnUser

from accounts.models import User
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from post.models import Magazine
from post.serializers import MagazineSerializer
from .permissions import IsWriterOrReadOnly

from .models import Region, Center, CenterReview, Cart, User, Report
from .models import Infra, Hobby, Lifestyle

from .serializers import RegionSerializer, CenterSerializer, CartSerializer, CartcostSerializer, ReportSerializer
from .serializers import FilterSerializer, CenterReviewSerializer, LifestyleSerializer, HobbySerializer, InfraSerializer

class Home(APIView):
    
    def get(self, request): # 홈화면
        # 지역 3개 랜덤 추천 리스트업
        # 해당 지역들의 매거진 하나씩 총 3개 리스트업
        length = len(Region.objects.all())
        region_id_list = random.sample(range(1, length+1), 3)
        region_list = []
        region_list.append(get_object_or_404(Region, id=region_id_list[0]))
        region_list.append(get_object_or_404(Region, id=region_id_list[1]))
        region_list.append(get_object_or_404(Region, id=region_id_list[2]))
        
        magazine_list = []
        # for region_id in region_id_list:
        #     magazines = Magazine.objects.filter(region_id=region_id)
        #     if magazines.exists():
        #         magazine = random.choice(magazines)
        #         magazine_list.append(magazine)
        
        region_id_list_example = [20, 34, 232]
        for region_id in region_id_list_example:
            magazines = Magazine.objects.filter(region_id=region_id)
            if magazines.exists():
                magazine = random.choice(magazines)
                magazine_list.append(magazine)

        region_serializer = RegionSerializer(region_list, many=True)
        magazine_serializer = MagazineSerializer(magazine_list, many=True)
        data = {
            'region_list': region_serializer.data,
            'magazine_list': magazine_serializer.data
        }
        print(data)

        return Response(data=data, status=status.HTTP_200_OK)

class Recommend(APIView):

    def post(self, request): # 입력한 주거 스타일을 받아오고 지역 추천 리스트 반환
        serializer = FilterSerializer(data=request.data) # 입력받은 인프라, 취미, 라이프스타일 값을 정수 리스트로 저장
        if serializer.is_valid():
            infra_values = serializer.validated_data.get('infra', []) # 입력받은 값이 없으면 빈 리스트[]를 반환
            hobby_values = serializer.validated_data.get('hobby', [])
            lifestyle_values = serializer.validated_data.get('lifestyle', [])

            regions = Region.objects.all()

            # 필터 조건 적용
            if infra_values:
                regions = regions.filter(infra_id__in=infra_values).distinct() # region의 infra_id가 infra_values 리스트에 포함된 객체들을 남기고 중복된 결과 제거
            if hobby_values:
                regions = regions.filter(hobby_id__in=hobby_values).distinct()
            if lifestyle_values:
                regions = regions.filter(lstyle_id__in=lifestyle_values).distinct()

            # 모든 지정된 Infra 값을 포함하는지 확인
            filtered_regions = []
            for region in regions:
                infra_ids = set(region.infra_id.values_list('id', flat=True))
                hobby_ids = set(region.hobby_id.values_list('id', flat=True))
                lifestyle_ids = set(region.lstyle_id.values_list('id', flat=True))

                if all(value in infra_ids for value in infra_values) and \
                   all(value in hobby_ids for value in hobby_values) and \
                   all(value in lifestyle_ids for value in lifestyle_values):
                    filtered_regions.append(region)

            region_serializer = RegionSerializer(filtered_regions, many=True)

            if not region_serializer.data:
                return Response({"message": "대상이 없습니다"}, status=status.HTTP_400_BAD_REQUEST)

            return Response(region_serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        infra_list = Infra.objects.all()
        hobby_list = Hobby.objects.all()
        lifestyle_list = Lifestyle.objects.all()
        
        infra_serializer = InfraSerializer(infra_list, many=True)
        hobby_serializer = HobbySerializer(hobby_list, many=True)
        lifestyle_serializer = LifestyleSerializer(lifestyle_list, many=True)
        
        combined_data = {
            'infra': infra_serializer.data,
            'hobby': hobby_serializer.data,
            'lifestyle': lifestyle_serializer.data
        }
        
        return Response(combined_data, status=status.HTTP_200_OK)

    # def post(self, request):
    #     serializer = FilterSerializer(data=request.data)
    #     if serializer.is_valid():
    #         filter_categories = {
    #             'infra': 'infra_id',
    #             'mood': 'mood_id',
    #             'housetype': 'htype_id'
    #         }

    #         query=Q()
    #         for key, value_list in serializer.validated_data.items():
    #             if key in filter_categories:
    #                 for value in value_list:
    #                     query &= Q(**{f"{filter_categories[key]}__id": value})

    #         regions = Region.objects.filter(query).distinct()
    #         region_serializer = RegionSerializer(regions, many=True)
    #         return Response(region_serializer.data, status=status.HTTP_200_OK)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegionInformation(APIView): # 각 지역의 정보 확인
     def get(self, request, id):
        city_code=id
        region= get_object_or_404(Region, city_code=city_code)
        serializer=RegionSerializer(region)
        return Response(serializer.data)
     
class CenterList(APIView): #해당되는 센터정보를 리스트로 보내줌.
    def get(self,request,id):

        city_code= id
        region=get_object_or_404(Region, city_code=city_code) #해당하는 지역 시티코드 받아올 수 있음.
        center_filter = Center.objects.filter(region_id=region.id)
        serializer=CenterSerializer(center_filter, many=True)
        return Response(serializer.data)
     
class CenterView(APIView):
    def get(self,request, id): # 특정 시설 개별 조회
        user = ReturnUser(request=request)
        center=get_object_or_404(Center,id=id)
        serializer=CenterSerializer(center)
        #region=get_object_or_404(Region,id=center.region_id)

        # 해당 유저가 이 시설을 저장했는지
        is_like = 0 # 저장했으면 1, 저장 안했으면 0
        if center in user.like_center.all(): is_like = 1

        if not serializer.data:
                return Response({"message": "대상이 없습니다"}, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.data
        data['is_like'] = is_like # 해당 유저가 이 시설을 저장했는지의 정보도 함께 반환
        return Response(data=data, status=status.HTTP_200_OK)

    def put(self, request, id): # 특정 시설 하나 저장 또는 저장 취소
        user = ReturnUser(request=request)
        center = get_object_or_404(Center, id=id)

        is_like = request.data.get('like') # 저장 눌렀으면 1, 안 눌렀으면 0
        if is_like: # 해당 시설을 저장
            user.like_center.add(center)
        else: # 해당 시설을 저장 취소
            user.like_center.remove(center)
        user.save()

        print(user.like_center)

        data = {
            'center_id': center.id,
            'user_id': user.id,
            'is_like': is_like,
            'user_like_center': [l_center.id for l_center in user.like_center.all()]
        }

        return Response(data=data, status=status.HTTP_200_OK)
    
class MyCartInsert(APIView):
    def post(self, request):
        center1_id = request.data.get('center1_id')
        center2_id = request.data.get('center2_id')
        center3_id = request.data.get('center3_id')
        center4_id = request.data.get('center4_id')
        center5_id = request.data.get('center5_id')

        center1 = center2 = center3 = center4 = center5 = None

        if center1_id:
            try:
                center1 = Center.objects.get(id=center1_id)
            except Center.DoesNotExist:
                return Response({"error": f"Center with id {center1_id} does not exist."}, status=status.HTTP_404_NOT_FOUND)

        if center2_id:
            try:
                center2 = Center.objects.get(id=center2_id)
            except Center.DoesNotExist:
                return Response({"error": f"Center with id {center2_id} does not exist."}, status=status.HTTP_404_NOT_FOUND)

        if center3_id:
            try:
                center3 = Center.objects.get(id=center3_id)
            except Center.DoesNotExist:
                return Response({"error": f"Center with id {center3_id} does not exist."}, status=status.HTTP_404_NOT_FOUND)

        if center4_id:
            try:
                center4 = Center.objects.get(id=center4_id)
            except Center.DoesNotExist:
                return Response({"error": f"Center with id {center4_id} does not exist."}, status=status.HTTP_404_NOT_FOUND)

        if center5_id:
            try:
                center5 = Center.objects.get(id=center5_id)
            except Center.DoesNotExist:
                return Response({"error": f"Center with id {center5_id} does not exist."}, status=status.HTTP_404_NOT_FOUND)

        # Cart 객체 생성
        cart = Cart.objects.create(
            center1=center1,
            center2=center2,
            center3=center3,
            center4=center4,
            center5=center5,
        )
        
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    # def post(self, request):
        
        # center1_id = request.data.get('center1_id')
        # center2_id = request.data.get('center2_id')
        # center3_id = request.data.get('center3_id')
        # center4_id = request.data.get('center4_id')
        # center5_id = request.data.get('center5_id')

        # if center1_id:
        #     center1 = Center.objects.get(id=center1_id)
        #     cart.center1 = center1

        # if center2_id:
        #     center2 = Center.objects.get(id=center2_id)
        #     cart.center2 = center2

        # if center3_id:
        #     center3 = Center.objects.get(id=center3_id)
        #     cart.center3 = center3

        # if center4_id:
        #     center4 = Center.objects.get(id=center4_id)
        #     cart.center4 = center4

        # if center5_id:
        #     center5 = Center.objects.get(id=center5_id)
        #     cart.center5 = center5

        # cart.save()
        # serializer = CartSerializer(cart)

        # cart = Cart.objects.create(center1=center1, center2=center2, center3=center3, center4=center4, center5=center5)
        # serializer = CartSerializer(cart)

        # return Response(serializer.data, status=status.HTTP_200_OK)

class MyCart(APIView):
    
    def put(self, request, id):
        try:
            cart = Cart.objects.get(id=id)
        except Cart.DoesNotExist:
            return Response({"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)
        
        delete_center = request.data.get('delete_center')
        if delete_center is not None:
            delete_center = int(delete_center)

            if delete_center == 1 and cart.center1:
                cart.center1 = None

            if delete_center == 2 and cart.center2:
                cart.center2 = None

            if delete_center == 3 and cart.center3:
                cart.center3 = None

            if delete_center == 4 and cart.center4:
                cart.center4 = None

            if delete_center == 5 and cart.center5:
                cart.center5 = None

        cart.save()
        serializer = CartSerializer(cart)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def get(self, request, id):
        try:
            cart = Cart.objects.get(id=id)
        except Cart.DoesNotExist:
            return Response({"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer=CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class MyReport(APIView):

    def post(self, request, id):
        mybudget = request.data.get('mybudget')
        if mybudget is None:
            return Response({"error": "Budget not provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        mybudget = float(mybudget)*0.057

        try:
            cart = Cart.objects.get(id=id)
        except Cart.DoesNotExist:
            return Response({"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer=CartcostSerializer(cart)
        cart_cost = float(serializer.data['total_cost'])

        if cart_cost >= mybudget:
            return Response({
                "message": "true",
                "나의 적정여가비용": mybudget,
                "내가 담은 여가비용": cart_cost
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "message": "false",
                "나의 적정여가비용": mybudget,
                "내가 담은 여가비용": cart_cost
            }, status=status.HTTP_200_OK)
        
class ReportWrite(APIView):
    def post(self, request):
        user = ReturnUser(request=request)
        if not hasattr(user, 'id'):  # User 객체가 아닌 경우를 확인합니다.
            return Response({"error": "User가 없습니다. 글쓰기 불가."}, status=status.HTTP_404_NOT_FOUND)
        
        plan1 = request.data.get('plan1')
        plan2 = request.data.get('plan2')
        plan3 = request.data.get('plan3')

        # if not plan1 or not plan2 or not plan3:
        #     return JsonResponse({"error": "모든 계획을 입력해야 합니다."}, status=400)
        
        city_code = request.data.get("city_code")
        if not city_code:
            return JsonResponse({"error": "City code를 입력해야 합니다."}, status=400)

        region = get_object_or_404(Region, city_code=city_code)

        data = {
            'user_id': user.id,
            'region_id': region.id,
            'plan1': plan1,
            'plan2': plan2,
            'plan3': plan3
        }

        serializer = ReportSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CenterReviewView(APIView):
    def post(self, request, id): # 해당 시설 후기 작성
        user = ReturnUser(request=request)

        data = {
            'center_id': id,
            'user_id': user.id,
            'nickname': user.nickname,
            'content': request.data.get('content'),
            'score': request.data.get('score'),
            'thumbnail': request.data.get('thumbnail')
        }

        serializer = CenterReviewSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, id): # 시설 후기 리스트업

        center_reviews = CenterReview.objects.filter(center_id=id) # 해당 시설의 후기들
        serializer = CenterReviewSerializer(center_reviews, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

class CenterReviewLookView(APIView):
    permission_classes = [IsWriterOrReadOnly]
    
    def get(self, request, id): # 시설 후기 개별 보기
        center_review = get_object_or_404(CenterReview, id=id)
        data = {
            'center_id': center_review.center_id.id,
            'user_id': center_review.user_id.id,
            'content': center_review.content,
            'score': request.data.get('score'),
            'thumbnail': request.data.get('thumbnail')
        }

        serializer = CenterReviewSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id): # 시설 후기 삭제
        center_review = get_object_or_404(CenterReview, id=id)
        self.check_object_permissions(self.request, center_review) # 해당 객체 permission 체크
        center_review.delete()
        return Response({"success": "시설 리뷰가 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)