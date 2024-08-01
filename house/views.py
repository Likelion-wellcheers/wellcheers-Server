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

from .models import Region, Center, CenterReview, Cart, User, Report

from .serializers import RegionSerializer, CenterSerializer, CartSerializer, CartcostSerializer
from .serializers import FilterSerializer, CenterReviewSerializer

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
        center=get_object_or_404(Center,id=id)
        serializer=CenterSerializer(center)
        #region=get_object_or_404(Region,id=center.region_id)

        if not serializer.data:
                return Response({"message": "대상이 없습니다"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data)

    def put(self, request, id): # 특정 시설 하나 저장 또는 저장 취소
        center = get_object_or_404(Center, id=id)
        token = request.data.get('access_token') # 엑세스 토큰으로 사용자 식별
        user = User.get_user_or_none_by_token(token=token)

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
    
class MyCart(APIView):

    def post(self, request):

        center1_id = request.data.get('center1_id')
        center2_id = request.data.get('center2_id')
        center3_id = request.data.get('center3_id')
        center4_id = request.data.get('center4_id')
        center5_id = request.data.get('center5_id')

        center1 = Center.objects.get(id=center1_id)
        center2 = Center.objects.get(id=center2_id)
        center3 = Center.objects.get(id=center3_id)
        center4 = Center.objects.get(id=center4_id)
        center5 = Center.objects.get(id=center5_id)

        cart = Cart.objects.create(center1=center1, center2=center2, center3=center3, center4=center4, center=center5)
        serializer = CartSerializer(cart)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, id):
        try:
            cart = Cart.objects.get(id=id)
        except Cart.DoesNotExist:
            return Response({"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)
        
        center1_id = request.data.get('center1_id')
        center2_id = request.data.get('center2_id')
        center3_id = request.data.get('center3_id')
        center4_id = request.data.get('center4_id')
        center5_id = request.data.get('center5_id')

        if center1_id:
            center1 = Center.objects.get(id=center1_id)
            cart.center1 = center1

        if center2_id:
            center2 = Center.objects.get(id=center2_id)
            cart.center2 = center2

        if center3_id:
            center3 = Center.objects.get(id=center3_id)
            cart.center3 = center3

        if center4_id:
            center4 = Center.objects.get(id=center4_id)
            cart.center4 = center4

        if center5_id:
            center5 = Center.objects.get(id=center5_id)
            cart.center5 = center5

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

        if cart_cost>=mybudget:
            return Response({"message": "true", 
                             "나의 적정여가비용": mybudget.data, 
                             "내가 담은 여가비용": cart_cost.data}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "false",
                             "나의 적정여가비용": mybudget.data, 
                             "내가 담은 여가비용": cart_cost.data},status=status.HTTP_200_OK)
        
class ReportWrite(APIView):
    def post(self, request):
        token = request.data.get('access_token') # 엑세스 토큰으로 사용자 식별
        user = User.get_user_or_none_by_token(token=token)
        if user is None: # 해당 토큰으로 식별된 유저가 없는 경우
            return Response({"error": "User 가 없습니다. 글쓰기 불가."}, status=status.HTTP_404_NOT_FOUND)
        
        plan1 = request.data.get('plan1')
        plan2 = request.data.get('plan2')
        plan3 = request.data.get('plan3')

        if not plan1 or not plan2 or not plan3:
            return JsonResponse({"error": "모든 계획을 입력해야 합니다."}, status=400)

        report = Report(user_id=user, plan1=plan1, plan2=plan2, plan3=plan3)
        report.save()

        return Response({
            "id": report.id,
            "user_id": report.user_id.id,
            "plan1": report.plan1,
            "plan2": report.plan2,
            "plan3": report.plan3,
        }, status=202)


class CenterReviewView(APIView):
    def post(self, request, id): # 해당 시설 후기 작성
        
        token = request.data.get('access_token') # 엑세스 토큰으로 사용자 식별
        user = User.get_user_or_none_by_token(token=token)

        data = {
            'center_id': id,
            'user_id': user.id,
            'content': request.data.get('content')
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