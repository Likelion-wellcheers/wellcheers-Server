from django.shortcuts import get_object_or_404, render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from accounts.views import ReturnUser

from house.models import Region
from accounts.models import User
from .permissions import IsWriterOrReadOnly
from .models import Question, Answer
from .serializers import QuestionSerializer, AnswerSerializer

# Create your views here.
class QnA(APIView):
    def post(self, request): # 지역과 질문을 입력하여 질문을 생성
        city = request.data.get('city')
        gugoon = request.data.get('gugoon')

        if not city :
            if not gugoon:
                return Response({"error": "시와 군,구를 모두 선택해주세요."}, status=status.HTTP_400_BAD_REQUEST)

        region = get_object_or_404(Region, city=city, gugoon=gugoon)
        user = ReturnUser(request=request)

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
    def get(self, request): # 해당 지역 질문글 리스트업
        user = ReturnUser(request=request)

        if user is None: # 해당 토큰으로 식별된 유저가 없는 경우
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        
        region_id = user.region_id.id # 해당 유저가 거주하는 지역 id
        questions = Question.objects.filter(region_id=region_id) # 해당 지역의 질문글
        serializer = QuestionSerializer(questions, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class QuestionDetail(APIView):
    permission_classes = [IsWriterOrReadOnly]

    def get(self, request, q_id): # 각 질문글 개별 보기

        question = get_object_or_404(Question, id=q_id) # 선택한 질문글
        serializer = QuestionSerializer(question)

        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, q_id): # 각 질문글에 답변하기
        
        user = ReturnUser(request=request)

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
    
    def put(self, request, q_id): # 주민들 궁금증 해결 여부 처리
        qna = get_object_or_404(Question, id=q_id)
        self.check_object_permissions(self.request, qna) # 해당 객체 permission 체크

        if request.data.get('is_finish') == 1: # 해결된 상태라면
            qna.finish = 1
        else: 
            qna.finish = 0
        serializer = QuestionSerializer(qna)

        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
class MyQuestion(APIView):
    def get(self, request): # 내가 작성한 질문 리스트업
        user = ReturnUser(request=request)
        user_id = user.id

        questions = Question.objects.filter(q_user_id=user_id) # 해당 유저가 작성한 질문글
        serializer = QuestionSerializer(questions, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

class MyAnswer(APIView):
    def get(self, request): # 내가 답변한 질문 리스트업
        user = ReturnUser(request=request)
        user_id = user.id

        answers = Answer.objects.filter(a_user_id=user_id) # 해당 유저의 답변들
        question_list = [] # 각 답변에 해당하는 질문글 리스트
        for answer in answers:
            question_list.append(answer.q_id)
        serializer = QuestionSerializer(question_list, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)