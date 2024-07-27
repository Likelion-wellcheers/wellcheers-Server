from django.db import models

class BaseModel(models.Model):
    created_at= models.DateTimeField(verbose_name="등록일시", auto_now_add=True)

    class Meta:
        abstract = True

# Create your models here.
class House_type (BaseModel):
    id=models.AutoField(primary_key=True)
    name=models.CharField(verbose_name="주거형태", max_length=20)

    def __str__(self):
        return self.name

class Infra (BaseModel):
    id=models.AutoField(primary_key=True)
    name=models.CharField(verbose_name="인프라", max_length=20)

    def __str__(self):
        return self.name

class Mood (BaseModel):
    id=models.AutoField(primary_key=True)
    name=models.CharField(verbose_name="분위기", max_length=20)

    def __str__(self):
        return self.name

class Region (BaseModel):
    id= models.AutoField(primary_key=True)
    htype_id=models.ManyToManyField(House_type, blank=True)
    infra_id=models.ManyToManyField(Infra, blank=True)
    mood_id=models.ManyToManyField(Mood, blank=True)
    city= models.CharField(verbose_name="시",max_length=20)
    gu= models.CharField(verbose_name="구",max_length=20, blank=True)
    goon= models.CharField(verbose_name="군",max_length=20, blank=True) #모델을 수정해서 null True 로 안해두면 migrations 기 안됨...

