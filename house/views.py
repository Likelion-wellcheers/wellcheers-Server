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

class Recommend(APIView):
    def get(self, request):
        infra        = request.GET.get('category', None)
        sub_category    = request.GET.get('subcategory', None)
        detail_category = request.GET.get('detailcategory', None)
        color           = request.GET.getlist('color', None)
        size            = request.GET.getlist('size', None)
        
        if category:
            products = Product.objects.filter(detail_category__sub_category__category=category)

        if sub_category:
            products = products.filter(detail_category__sub_category=sub_category)

        if detail_category:
            products = products.filter(detail_category=detail_category)

        if color:
            products = products.filter(productoption__color__in=color).distinct()

        if size:
            products = products.filter(productoption__size__in=size).distinct()
    


# Create your views here.
