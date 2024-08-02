# accounts/urls.py
from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    # 회원가입/로그인/로그아웃
    path("join/", RegisterView.as_view()), # 회원가입
    path("login/", AuthView.as_view()), # 로그인
    path("logout/", LogoutView.as_view()), # 로그아웃

    # 토큰
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"), # refresh token을 입력하면 access token을 반환
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),

    # 카카오 소셜 로그인
    path("kakao/login/", KakoLoginView.as_view(), name="kakao_login"),
    path("kakao/callback/", KakaoCallbackView.as_view(), name="kakao_callback"),

    # 사용자 추가 정보 입력
    path("region/", ChoiceRegion.as_view(), name='choiceregion.군구보여줌'),
    path("information/", AddUserInfo.as_view(), name="user_information"),

    # 사용자 내 정보 보기/수정
    path("mypage/", MyPage.as_view(), name="user_mypage"),
    path("mypage/plan/", MyPagePlan.as_view(), name="user_mypage_plan"),
    path("mypage/like/", MyPageLike.as_view(), name="user_mypage_like"),
    path("mypage/regionreview/", MyPageRegionReview.as_view(), name="user_mypage_regionreview"),
    path("mypage/centerreview/", MyPageCenterReview.as_view(), name="user_mypage_centerreview"),
]