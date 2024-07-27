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

from .models import Region
from .serializers import RegionSerializer
from .serializers import FilterSerializer

class Recommend(APIView):

    def post(self, request):
        serializer = FilterSerializer(data=request.data)
        if serializer.is_valid():
            infra_values = serializer.validated_data.get('infra', [])
            mood_values = serializer.validated_data.get('mood', [])
            housetype_values = serializer.validated_data.get('housetype', [])

            regions = Region.objects.all()

            # 필터 조건 적용
            if infra_values:
                regions = regions.filter(infra_id__in=infra_values).distinct()
            if mood_values:
                regions = regions.filter(mood_id__in=mood_values).distinct()
            if housetype_values:
                regions = regions.filter(htype_id__in=housetype_values).distinct()

            # 모든 지정된 Infra 값을 포함하는지 확인
            filtered_regions = []
            for region in regions:
                infra_ids = set(region.infra_id.values_list('id', flat=True))
                if all(value in infra_ids for value in infra_values):
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
