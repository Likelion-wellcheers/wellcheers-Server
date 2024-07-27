from django.db import models

class BaseModel(models.Model):
    created_at= models.DateTimeField(verbose_name="등록일시", auto_now_add=True)

    class Meta:
        abstract = True

# Create your models here.
class Lifestyle (BaseModel):
    id=models.AutoField(primary_key=True)
    name=models.CharField(verbose_name="라이프스타일", max_length=20)

    def __str__(self):
        return f"{self.id} - {self.name}"

class Infra (BaseModel):
    id=models.AutoField(primary_key=True)
    name=models.CharField(verbose_name="인프라", max_length=20)

    def __str__(self):
        return f"{self.id} - {self.name}"

class Hobby (BaseModel):
    id=models.AutoField(primary_key=True)
    name=models.CharField(verbose_name="여가활동", max_length=20)

    def __str__(self):
        return f"{self.id} - {self.name}"

class Region (BaseModel):
    id= models.AutoField(primary_key=True)
    lstyle_id=models.ManyToManyField(Lifestyle, blank=True)
    infra_id=models.ManyToManyField(Infra, blank=True)
    hobby_id=models.ManyToManyField(Hobby, blank=True)
    city= models.CharField(verbose_name="시",max_length=20)
    gu= models.CharField(verbose_name="구",max_length=20, blank=True)
    goon= models.CharField(verbose_name="군",max_length=20, blank=True) #모델을 수정해서 null True 로 안해두면 migrations 기 안됨...

    def __str__(self):
        return f"{self.id} - {self.city}-{self.gu}"

class Center (BaseModel):
    id=models.AutoField(primary_key=True)
    name=models.CharField(verbose_name="센터명",max_length=20)
    region_id= models.ForeignKey(Region, verbose_name="지역", on_delete=models.CASCADE)
    address=models.TextField(verbose_name="상세주소")
    time=models.CharField(verbose_name="운영시간정보",blank=True, max_length=150)
    cost=models.IntegerField(verbose_name="이용비용")

    def __str__(self):
        return f"{self.id} - {self.name}"

class CenterReview(BaseModel):
    id=models.AutoField(primary_key=True)
    center_id=models.ForeignKey(Center, verbose_name="시설",on_delete=models.CASCADE)
    #user_id=models.ForeignKey() # User 가 연결이 안되어있어 아직 주석처리.
    content=models.CharField(verbose_name="후기내용", max_length=150) #일단은 150자 이내로 쓰게함

