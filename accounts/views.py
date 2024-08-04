from django.shortcuts import get_object_or_404, redirect, render
import logging

def ReturnUser(request): # 헤더에 입력된 토큰으로 유저를 반환하는 메소드
    bearer_token = request.headers.get('Authorization') # 엑세스 토큰으로 사용자 식별
    if bearer_token is None:
        return Response({"error": "Authorization header missing."}, status=status.HTTP_401_UNAUTHORIZED)

    token = bearer_token.split('Bearer ')[-1] # 토큰만 가져옴
    user = User.get_user_or_none_by_token(token=token)

    return user

# Create your views here.

from rest_framework_simplejwt.serializers import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from accounts.models import PursueLifestyle
from accounts.serializers import *
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout

from house.models import CenterReview, Region, Report
from house.serializers import CenterReviewSerializer, CenterSerializer, ReportSerializer
from post.models import Review
from post.serializers import ReviewSerializer

class RegisterView(APIView):

    def post(self, request): # 회원가입 수행
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.save(request)
            token = RefreshToken.for_user(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "register success",
                    "token": {
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                    },
                },
                status=status.HTTP_201_CREATED,
            )
            return res
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class AuthView(APIView):

    def post(self, request): # 로그인 수행
        serializer = AuthSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data["user"]
            access_token = serializer.validated_data["access_token"]
            refresh_token = serializer.validated_data["refresh_token"]
            res = Response(
                {
                    "user": {
                        "id": user.id,
                        "email": user.email,
                    },
                    "message": "login success",
                    "token": {
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
            res.set_cookie("access-token", access_token, httponly=True)
            res.set_cookie("refresh-token", refresh_token, httponly=True)
            return res
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"message": "로그아웃되었습니다."}, status=status.HTTP_200_OK)

from pathlib import Path
import os, json
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent
secret_file = os.path.join(BASE_DIR, "secrets.json")

with open(secret_file) as f:
    secrets = json.loads(f.read())

def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)

KAKAO_REST_API_KEY = get_secret("KAKAO_REST_API_KEY") # REST API를 호출할 때 사용함
KAKAO_REDIRECT_URI = "https://youknowhoknow.netlify.app/kakaologin"
KAKAO_CLIENT_SECRET_KEY = get_secret("KAKAO_CLIENT_SECRET_KEY") # admin키. 모든 권한을 가지고 있는 키. 노출이 되지 않도록 주의 필요
KAKAO_LOGIN_URI = get_secret("KAKAO_LOGIN_URI") # 로그인 페이지 주소 -> 인가 코드 받기
KAKAO_TOKEN_URI = get_secret("KAKAO_TOKEN_URI") # 액세스 토큰 발급받기 위한 주소
KAKAO_PROFILE_URI = get_secret("KAKAO_PROFILE_URI") # 프로필 정보 조회를 위한 주소

from rest_framework.permissions import AllowAny
import requests

class KakoLoginView(APIView): # 카카오 로그인
    permission_classes = (AllowAny,) # 모든 사용자 접근 허용

    def get(self, request): # 사용자가 로그인 테스트 서버로 접속시 redirect URI를 반환
        '''
        kakao code 요청
        '''
        client_id = KAKAO_REST_API_KEY
        redirect_uri = KAKAO_REDIRECT_URI

        uri = f"{KAKAO_LOGIN_URI}?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}"
        
        res = redirect(uri)
        return res

class KakaoCallbackView(APIView): # 카카오 Callback
    parser_classes = (AllowAny,) # 모든 사용자 접근 허용

    def post(self, request): # 사용자가 oauth 로그인시 code 검증 및 로그인 처리
        '''
        kakao access_token 요청 및 user_info(사용자 정보) 요청
        '''
        # data = request.query_params.copy() # 쿼리 파라미터에서 authorization code를 추출

        # access_token 발급 요청
        # code = data.get('code')
        code = request.data.get('code')
        print(code)
        logging.log(code)
        
        if not code:
            return Response(status=status.HTTP_400_BAD_REQUEST) # code가 없는 경우 잘못된 요청 응답 반환
        
        # Kakao의 access_token 발급 요청을 위한 데이터 구성
        request_data = {
            'grant_type': 'authorization_code',
            'client_id': KAKAO_REST_API_KEY,  # Kakao API 키
            'redirect_uri': KAKAO_REDIRECT_URI,  # Kakao 리다이렉트 URI
            'client_secret': KAKAO_CLIENT_SECRET_KEY,  # Kakao 클라이언트 비밀키
            'code': code,  # 받은 authorization code
        }
        # 요청 헤더 설정
        token_headers = {
            'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'
        }
        # Kakao 토큰 발급 엔드포인트에 POST 요청을 보냄
        token_res = requests.post(KAKAO_TOKEN_URI, data=request_data, headers=token_headers)

        token_json = token_res.json() # 응답을 JSON 형식으로 파싱

        access_token = token_json.get('access_token')
        refresh_token = token_json.get('refresh_token')

        if not access_token: # access_token이 없는 경우, 잘못된 요청 응답을 반환
            return Response(status=status.HTTP_400_BAD_REQUEST)
        access_token = f"Bearer {access_token}"  # 'Bearer ' 마지막 띄어쓰기 필수

        # kakao 회원정보 요청
        auth_headers = { # 카카오 사용자 정보 요청을 위한 인증 헤더 설정
            "Authorization": access_token,
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
        }

        # kakao 사용자 정보 엔드포인터에 GET 요청을 보냄
        user_info_res = requests.get(KAKAO_PROFILE_URI, headers=auth_headers)
        user_info_json = user_info_res.json() # 응답을 JSON 형식으로 파싱

        # 소셜 타입 및 소셜 ID 생성
        social_type = 'kakao'
        social_id = f"{social_type}_{user_info_json.get('id')}"

        # Kakao 계정 정보 가져옴
        kakao_account = user_info_json.get('kakao_account')
        if not kakao_account: # 카카오 계정이 없다면
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user_email = kakao_account.get('email')

        # 사용자의 프로필 정보 받아옴
        user_profile = kakao_account.get('profile')
        user_name = user_profile.get('nickname')
        user_profileimage_url = user_profile.get('profile_image_url')

        '''
        회원가입 및 로그인 처리 알고리즘
        # 내부 시스템 회원가입 또는 로그인 처리
        '''
        
        # 이미 존재하는 유저라면 로그인 처리
        user = User.get_user_or_none_by_email(email=user_email)
        if user is None:
            # 존재하지 않는 유저라면 회원가입 처리
            user = User.objects.create(
                username = user_name,
                email = user_email,
                profileimage_url = user_profileimage_url
            )
            user.set_password("1234") # 임의의 값으로 비밀번호 설정
            user.save()
        else: # 바뀐 정보가 있다면 업데이트
            user.username = user_name
            user.email = user_email
            user.profileimage_url = user_profileimage_url
            user.save()

        token = RefreshToken.for_user(user)
        internal_refresh_token = str(token) # 내부 refresh token 반환
        internal_access_token = str(token.access_token) # 내부 access 토큰 반환

        # 반환 값
        res = {
            'internal_access_token': internal_access_token,
            'internal_refresh_token': internal_refresh_token
        }
        response = Response(data=res, status=status.HTTP_200_OK)
        return response

class AddUserInfo(APIView):
    def put(self, request): # 사용자 추가정보 입력
        user = ReturnUser(request=request)
        if user is None: # 해당 이메일을 가진 유저가 없는 경우
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        user.nickname = request.data.get('nickname')
        city = request.data.get('city')
        gugoon = request.data.get('gugoon', user.gugoon) # 입력이 없으면 기존값 유지
        user.city = city
        user.gugoon = gugoon
        user.region_id = get_object_or_404(Region, city=city, gugoon=gugoon)
        
        # pursue_lifestyle_id 처리
        pursue_lifestyle_ids = request.data.get('pursue_lifestyle_id', []) # 입력된 id를 모두 받아와 리스트에 저장
        if pursue_lifestyle_ids:
            # 기존의 라이프스타일을 모두 제거하고 새로운 값으로 설정
            user.pursue_lifestyle_id.clear()
            for pursue_lifestyle_id in pursue_lifestyle_ids:
                try:
                    pursue_lifestyle = PursueLifestyle.objects.get(id=pursue_lifestyle_id)
                    user.pursue_lifestyle_id.add(pursue_lifestyle)
                except PursueLifestyle.DoesNotExist:
                    return Response({"error": f"PursueLifestyle id {pursue_lifestyle_id} not found."}, status=status.HTTP_400_BAD_REQUEST)

        user.save()

        res = {
            'username': user.username,
            'email': user.email,
            'nickname': user.nickname,
            'city': user.city,
            'gugoon': user.gugoon,
            'region_id': user.region_id.id,
            'pursue_lifestyle': [pl.id for pl in user.pursue_lifestyle_id.all()]
        }
        return Response(data=res, status=status.HTTP_200_OK)

class ChoiceRegion(APIView):
    def post(self, request): # 시를 입력하면 그 시의 군구 citycode들을 반환
        city = request.data.get('city')
        if not city:
            return Response({"error": "시 또는 도를 선택해주세요."}, status=status.HTTP_400_BAD_REQUEST)

        choice_regions = Region.objects.filter(city=city) #해당 city 를 갖고있는 지역 개체들 불러오기
        gugoon = Region.objects.filter(city=city).values_list('gugoon', flat=True).distinct()
        #goon = Region.objects.filter(city=city).values_list('goon', flat=True).distinct() 모델수정전

        region_data = list(choice_regions.values()) #여러개일테니까 데이터값을 리스트로 불러옴.
        citycodes = [region.get('city_code') for region in region_data]

        return Response({
            "city":city,
            "gugoon": list(gugoon),
            #"goon": list(goon),
            "city_codes": citycodes # 걸러진 region 의 city_code 값과 해당되는 구군 이름도 따로 보내줌
        }, status=status.HTTP_200_OK)

class MyPage(APIView):
    def get(self, request): # 사용자 내 정보 확인
        user = ReturnUser(request=request)

        if user is None: # 해당 토큰으로 식별된 유저가 없는 경우
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UserSerializer(user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request): # 사용자 내 정보 수정
        user = ReturnUser(request=request)

        if user is None: # 해당 토큰으로 식별된 유저가 없는 경우
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        
        city = request.data.get('city')
        gugoon = request.data.get('gugoon', user.gugoon) # 입력이 없으면 기존값 유지
        user.city = city
        user.gugoon = gugoon
        user.region_id = get_object_or_404(Region, city=city, gugoon=gugoon)

        serializer = UserSerializer(user, data=request.data, partial=True) # 원하는 값만 업데이트
        if serializer.is_valid(): # update니까 유효성 검사 필요
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MyPageRegionReview(APIView):
    def get(self, request): # 해당 사용자가 작성한 지역 후기 리스트업
        user = ReturnUser(request=request)

        if user is None: # 해당 토큰으로 식별된 유저가 없는 경우
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        
        region_reviews = Review.objects.filter(user_id=user.id) # 해당 사용자가 작성한 지역 후기들
        serializer = ReviewSerializer(region_reviews, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

class MyPageCenterReview(APIView):
    def get(self, request): # 해당 사용자가 작성한 시설 후기 리스트업
        user = ReturnUser(request=request)

        if user is None: # 해당 토큰으로 식별된 유저가 없는 경우
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        
        center_review = CenterReview.objects.filter(user_id=user.id) # 해당 사용자가 작성한 지역 후기들
        serializer = CenterReviewSerializer(center_review, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

class MyPageLike(APIView):
    def get(self, request): # 해당 사용자가 저장한 시설(지역으로 묶어서) 리스트업
        user = ReturnUser(request=request)

        if user is None: # 해당 토큰으로 식별된 유저가 없는 경우
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        
        like_centers = user.like_center.all()
        region_center_all = dict()
        for center in like_centers:
            region_id = str(center.region_id)  # 해당 시설의 지역 id값을 문자열로 변환하여 dict에 넣음
            if region_id in region_center_all: # 해당 지역 id가 dict에 있다면
                region_center_all[region_id].append(center)
            else:
                region_center_all[region_id] = [center]
        # print(region_center_all)

        # 지역별로 묶인 시설 목록을 시리얼라이저에 맞게 변환
        serialized_data = {}
        for region_id, centers in region_center_all.items():
            serialized_data[region_id] = CenterSerializer(centers, many=True).data

        return Response(data=serialized_data, status=status.HTTP_200_OK)

class MyPagePlan(APIView):
    def get(self, request): # 해당 사용자가 작성한 계획 리스트업
        user = ReturnUser(request=request)
        
        if user is None: # 해당 토큰으로 식별된 유저가 없는 경우
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        
        my_plans = Report.objects.filter(user_id=user.id) # 해당 유저가 작성한 계획들
        serializer = ReportSerializer(my_plans, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)