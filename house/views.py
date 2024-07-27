from django.shortcuts import render
from django.http import JsonResponse # 추가 
from django.shortcuts import get_object_or_404 # 추가
from django.views.decorators.http import require_http_methods
from .models import Post , Comment
import json
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.views import status
from rest_framework import status
from django.http import Http404
from rest_framework.decorators import api_view, permission_classes
import boto3

from .models import Region
from .serializers import RegionSerializer

class RegionByInfraView(APIView):
    def post(self, request, *args, **kwargs):
        infra_ids = request.data.get('infra_ids', []) #인프라 아이디로 입력을 받아옴.
        if not infra_ids:
            return Response({"error": "No infra_ids provided"}, status=status.HTTP_400_BAD_REQUEST) #인프라 입력이 안되면 오류 리턴

        regions = Region.objects.all()
        infra_count = len(infra_ids)

        # Filter regions that contain the maximum number of specified infra
        filtered_regions = []
        for region in regions:
            infra_set = set(region.infra_id.values_list('id', flat=True))
            common_infra = infra_set.intersection(infra_ids)
            if common_infra:
                filtered_regions.append((region, len(common_infra)))

        # Sort regions by the number of matching infra in descending order
        filtered_regions.sort(key=lambda x: x[1], reverse=True)

        if filtered_regions:
            max_infra_count = filtered_regions[0][1]
            max_regions = [region for region, count in filtered_regions if count == max_infra_count]
        else:
            max_regions = []

        region_serializer = RegionSerializer(max_regions, many=True)
        return Response(region_serializer.data, status=status.HTTP_200_OK)
    

    
# Create your views here.
