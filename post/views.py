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
from .serializers import Articleserializer

class AtriclePost(APIView):
        def get(self, request, format=None):
            articles=Article.objects.all()
            serializers=Articleserializer(articles, many=True)
            return Response(serializers.data)