from django.db import models
from accounts.models import User
from house.models import Region

class BaseModel(models.Model):
    created_at= models.DateTimeField(verbose_name="등록일시", auto_now_add=True)

    class Meta:
        abstract = True

# Create your models here.
class Request (BaseModel): #요청하기글 모델입니다
    id=models.AutoField(primary_key=True)
    user_id=models.ForeignKey(User, verbose_name="작성자", on_delete=models.CASCADE, null=True)
    region_id = models.ForeignKey(Region, verbose_name="지역", on_delete=models.CASCADE)
    finish=models.BooleanField(default=False)
    content=models.TextField(verbose_name="내용")
    title=models.CharField(verbose_name="제목", max_length=50)

class Article(BaseModel): #이 모델이 복지정책 모델입니다.
    id=models.AutoField(primary_key=True)
    region_id = models.ForeignKey(Region, verbose_name="지역", on_delete=models.CASCADE)
    image=models.ImageField(verbose_name="이미지")
    content=models.TextField(verbose_name="내용",  blank=True)
    
class Magazine(BaseModel): # 매거진 관련모델. 
    id=models.AutoField(primary_key=True)
    region_id = models.ForeignKey(Region, verbose_name="지역", on_delete=models.CASCADE)
    image=models.ImageField(verbose_name="이미지")
    content=models.TextField(verbose_name="내용",  blank=True)

class Review(BaseModel): # 동네후기 모델입니다. 텍스트 비워둘 수 없음. 이미지 안올릴 수 있음.
    id=models.AutoField(primary_key=True)
    user_id=models.ForeignKey(User, verbose_name="작성자", on_delete=models.CASCADE, null=True)
    region_id = models.ForeignKey(Region, verbose_name="지역", on_delete=models.CASCADE)
    content=models.TextField(verbose_name="내용")
    score=models.IntegerField(verbose_name="별점")
    image=models.ImageField(verbose_name="이미지", blank=True)

#Create your models here.
