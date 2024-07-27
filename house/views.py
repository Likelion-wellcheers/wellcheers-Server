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

from .models import Region, Center, CenterReview
from .serializers import RegionSerializer, CenterSerializer
from .serializers import FilterSerializer

class Recommend(APIView):

    def post(self, request):
        serializer = FilterSerializer(data=request.data)
        if serializer.is_valid():
            infra_values = serializer.validated_data.get('infra', [])
            hobby_values = serializer.validated_data.get('hobby', [])
            lifestyle_values = serializer.validated_data.get('lifestyle', [])

            regions = Region.objects.all()

            # 필터 조건 적용
            if infra_values:
                regions = regions.filter(infra_id__in=infra_values).distinct()
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

class RegionInformation(APIView):
     def get(self, request, id):
        region= get_object_or_404(Region, id=id)
        serializer=RegionSerializer(region)
        return Response(serializer.data)
     
class CenterList(APIView): #해당되는 센터정보를 리스트로 보내줌.
    def get(self,request,id):
        region=get_object_or_404(Region, id=id) #해당하는 지역 아이디 받아올 수 있음.
        center_filter = Center.objects.filter(region_id=region.id)
        serializer=CenterSerializer(center_filter, many=True)
        return Response(serializer.data)
     
class CenterView(APIView):
    def get(self,request, id):
        center=get_object_or_404(Center,id=id)
        serializer=CenterSerializer(center)
        
        if not serializer.data:
                return Response({"message": "대상이 없습니다"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data)

