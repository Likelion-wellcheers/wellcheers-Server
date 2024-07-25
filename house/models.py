from django.db import models

class BaseModel(models.Model):
    created_at= models.DateTimeField(verbose_name="등록일시", auto_now_add=True)

    class Meta:
        abstract = True

# Create your models here.
class House_type (BaseModel):
    id=models.AutoField(primary_key=True)
    name=models.CharField(verbose_name="주거형태", max_length=20)

class Infra (BaseModel):
    id=models.AutoField(primary_key=True)
    name=models.CharField(verbose_name="인프라", max_length=20)

class Mood (BaseModel):
    id=models.AutoField(primary_key=True)
    name=models.CharField(verbose_name="분위기", max_length=20)

class Region (BaseModel):
    id= models.AutoField(primary_key=True)
    htype_id=models.ManyToManyField(House_type, blank=True)
    infra_id=models.ManyToManyField(Infra, blank=True)
    mood_id=models.ManyToManyField(Mood, blank=True)
    city= models.CharField(verbose_name="시",max_length=20)
    gu= models.CharField(verbose_name="구",max_length=20)
    dong= models.CharField(verbose_name="동",max_length=20)

class House(BaseModel):
    id=models.AutoField(primary_key=True)
    region_id=models.ForeignKey(Region,on_delete=models.CASCADE)
    name=models.CharField(verbose_name="이름", max_length=50)
    location=models.CharField(verbose_name="위치", max_length=100)
    photo=models.ImageField()
    deposit=models.IntegerField() # 보증금/매매가/전세 등을 의미함.
    price=models.IntegerField() #월세를 의미함 
    pyong=models.IntegerField()

class SilverTown(BaseModel):
    id=models.AutoField(primary_key=True)
    region_id=models.ForeignKey(Region,on_delete=models.CASCADE)
    name=models.CharField(verbose_name="이름", max_length=50)
    size=models.IntegerField()  #크기 중형 소형 대형 파라미터 값.
    location=models.CharField(verbose_name="위치", max_length=100)
    SilverTown_Service_id=models.ManyToManyField(House_type, blank=True)

class SilverTown_Service(BaseModel):
    id=models.AutoField(primary_key=True)
    name=models.CharField(verbose_name="서비스명", max_length=20)

class House_Surroundings(BaseModel):
    id=models.AutoField(primary_key=True)
    house_id=models.ForeignKey(House, on_delete=models.CASCADE)
    region_id=models.ForeignKey(Region, on_delete=models.CASCADE)
    name=models.CharField(verbose_name="집 주변 정보", max_length=20)
    distance=models.IntegerField()


