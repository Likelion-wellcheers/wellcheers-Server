
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    city = models.CharField(verbose_name='시', max_length=20, blank=True)
    gu = models.CharField(verbose_name='구', max_length=20, blank=True)
    goon = models.CharField(verbose_name='군', max_length=20, blank=True)

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