
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass

    @staticmethod
    def get_user_or_none_by_username(username): # username값으로 해당 유저를 찾는 모델 내부 함수 
        try:
            return User.objects.get(username=username)
        except Exception:
            return None