from django.db import models
from accounts.models import User
from house.models import Region

class BaseModel(models.Model):
    created_at= models.DateTimeField(verbose_name="등록일시", auto_now_add=True)

    class Meta:
        abstract = True

# Create your models here.

class Article(BaseModel): #이 모델이 복지정책 모델입니다.
    id=models.AutoField(primary_key=True)
    region_id = models.ForeignKey(Region, verbose_name="지역", on_delete=models.CASCADE)
    image=models.ImageField(verbose_name="이미지",blank=True)
    content=models.TextField(verbose_name="내용",  blank=True)
    
class Magazine(BaseModel): # 매거진 관련모델. 
    id=models.AutoField(primary_key=True)
    region_id = models.ForeignKey(Region, verbose_name="지역", on_delete=models.CASCADE)
    image=models.ImageField(verbose_name="썸네일",blank=True)
    content=models.TextField(verbose_name="내용",  blank=True)

class MagazinePhoto(models.Model):
    id = models.AutoField(primary_key=True)
    magazine = models.ForeignKey(Magazine, related_name='photos', on_delete=models.CASCADE, null=True, blank=True)
    image=models.ImageField(verbose_name="글이미지",blank=True)

class Review(BaseModel): # 지역후기 모델입니다. 텍스트 비워둘 수 없음. 이미지 안올릴 수 있음.
    id=models.AutoField(primary_key=True)
    user_id=models.ForeignKey(User, verbose_name="작성자", on_delete=models.CASCADE, null=True)
    region_id = models.ForeignKey(Region, verbose_name="지역", on_delete=models.CASCADE)
    content=models.TextField(verbose_name="내용")
    score=models.IntegerField(verbose_name="별점")
    image=models.ImageField(verbose_name="이미지", blank=True, null=True)

    def city(self):
        return self.region_id.city
    
    def gugoon(self):
        return self.region_id.gugoon