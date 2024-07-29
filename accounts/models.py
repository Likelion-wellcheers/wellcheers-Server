from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

# Create your models here.
class PursueLifestyle(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name='추구하는 라이프스타일', max_length=30)


class User(AbstractUser):
    nickname = models.CharField(verbose_name="닉네임", max_length=10, blank=True)
    city = models.CharField(verbose_name='시', max_length=20, blank=True)
    gu = models.CharField(verbose_name='구', max_length=20, blank=True)
    goon = models.CharField(verbose_name='군', max_length=20, blank=True)
    pursue_lifestyle_id = models.ManyToManyField(PursueLifestyle, blank=True)

    @staticmethod
    def get_user_or_none_by_username(username): # username값으로 해당 유저를 찾는 모델 내부 함수 
        try:
            return User.objects.get(username=username)
        except Exception:
            return None
    
    @staticmethod
    def get_user_or_none_by_email(email): # email값으로 해당 유저를 찾는 모델 내부 함수
        try:
            return User.objects.get(email=email)
        except Exception:
            return None
    
    
    @staticmethod
    def get_user_or_none_by_token(token): # token값으로 해당 유저를 찾는 모델 내부 함수
        # jwt 토큰 디코딩
        try:
            # UntypedToken을 사용하여 토큰을 디코딩
            untoken = UntypedToken(token)

            # 토큰이 유효하면 데이터(payload)를 저장
            payload = untoken.payload
            if not payload: return None

            user_id = payload.get('user_id') # 토큰에서 유저 이메일 값을 가져옴
            print(payload)
            if not user_id:
                print('해당 토큰을 가진 유저가 없습니다.')
                return None
            
            return User.objects.get(id=user_id)

        except (InvalidToken, TokenError) as e:
            # 토큰이 유효하지 않으면 예외 처리
            print(f"토큰이 유효하지 않습니다.: {e}")
            return None