from django.shortcuts import get_object_or_404, render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from house.models import Region
from accounts.models import User
from .serializers import QuestionSerializer

# Create your views here.
class QnA(APIView):
    def post(self, request): # 지역과 질문을 입력하여 질문을 생성
        city = request.data.get('city')
        gu = request.data.get('gu')
        goon = request.data.get('goon')

        if not city :
            if not gu and goon:
                return Response({"error": "시와 군,구를 모두 선택해주세요."}, status=status.HTTP_400_BAD_REQUEST)

        region = get_object_or_404(Region, city=city, gu=gu, goon=goon)
        token = request.data.get('access_token') # 엑세스 토큰으로 사용자 식별
        user = User.get_user_or_none_by_token(token=token)

        data = {
            'q_user_id': user.id,
            'region_id': region.id,
            'title': request.data.get('title'),
            'content': request.data.get('content', ""),
            'image': request.data.get('image'),
            'finish': False
        }
        
        serializer = QuestionSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
