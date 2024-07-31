from django.shortcuts import get_object_or_404, render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from house.models import Region
from accounts.models import User
from .models import Question
from .serializers import QuestionSerializer, AnswerSerializer

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
    
class QuestionList(APIView):
    def get(self, request, region_id): # 해당 지역 질문글 리스트업

        questions = Question.objects.filter(region_id=region_id) # 해당 지역의 질문들
        serializer = QuestionSerializer(questions, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

class QuestionDetail(APIView):
    def get(self, request, q_id): # 각 질문글 개별 보기

        question = get_object_or_404(Question, id=q_id) # 선택한 질문글
        serializer = QuestionSerializer(question)

        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, q_id): # 각 질문글에 답변하기
        
        token = request.data.get('access_token') # 엑세스 토큰으로 사용자 식별
        user = User.get_user_or_none_by_token(token=token)

        data = { # 'q_id', 'a_user_id', 'content'
            'q_id' : q_id,
            'a_user_id' : user.id,
            'content' : request.data.get('content')
        }

        serializer = AnswerSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class MyQuestion(APIView):
    def get(self, request): # 내가 작성한 질문 리스트업
        token = request.data.get('access_token') # 엑세스 토큰으로 사용자 식별
        user = User.get_user_or_none_by_token(token=token)
        user_id = user.id

        questions = Question.objects.filter(q_user_id=user_id) # 해당 유저가 작성한 질문글
        serializer = QuestionSerializer(questions, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)