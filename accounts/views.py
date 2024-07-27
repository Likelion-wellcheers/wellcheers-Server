from django.shortcuts import redirect, render

# Create your views here.

from rest_framework_simplejwt.serializers import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from accounts.serializers import *
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout

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
KAKAO_REDIRECT_URI = get_secret("KAKAO_REDIRECT_URI")
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

    def get(self, request): # 사용자가 oauth 로그인시 code 검증 및 로그인 처리
        '''
        kakao access_token 요청 및 user_info(사용자 정보) 요청
        '''
        data = request.query_params.copy() # 쿼리 파라미터에서 authorization code를 추출

        # access_token 발급 요청
        code = data.get('code')
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
        if not kakao_account:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user_email = kakao_account.get('email')

        '''
        # 회원가입 및 로그인 처리 알고리즘 추가필요
        '''

        # 테스트 값 확인용
        res = {
            'social_type': social_type,
            'social_id': social_id,
            'user_email': user_email,
        }
        response = Response(status=status.HTTP_200_OK)
        response.data = res
        return res