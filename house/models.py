from django.db import models
from accounts.models import User

class BaseModel(models.Model):
    created_at= models.DateTimeField(verbose_name="등록일시", auto_now_add=True, blank=True)

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
    city_code=models.IntegerField(verbose_name="프론트파일 도시코드", blank=True)
    city= models.CharField(verbose_name="시 또는 도 ",max_length=20)
    gugoon= models.CharField(verbose_name="구 또는 군",max_length=20, blank=True)
    longtitude=models.DecimalField(verbose_name="겅도",max_digits=15, decimal_places=10, blank=True)
    latitude=models.DecimalField(verbose_name="위도",max_digits=15, decimal_places=10, blank= True)
    thumbnail = models.ImageField(null=True, blank=True, verbose_name="썸네일")


    def __str__(self):
        return f"{self.id} - {self.city}-{self.gugoon}"
    

class Center (BaseModel):
    id=models.AutoField(primary_key=True)
    name=models.CharField(verbose_name="센터명",max_length=20)
    region_id= models.ForeignKey(Region, verbose_name="지역", on_delete=models.CASCADE)
    address=models.TextField(verbose_name="상세주소")
    time=models.CharField(verbose_name="운영시간정보",blank=True, max_length=150)
    cost=models.IntegerField(verbose_name="이용비용",blank=True)
    longtitude=models.DecimalField(verbose_name="겅도",max_digits=15, decimal_places=10, blank=True)
    latitude=models.DecimalField(verbose_name="위도",max_digits=15, decimal_places=10, blank= True)
    thumbnail = models.ImageField(null=True, blank=True, verbose_name="썸네일") #필로우 깔아줘서 이미지필드 사용가능
    phonenum=models.CharField(null=True, blank=True, verbose_name="전화번호", max_length=15)

    def __str__(self):
        return f"{self.id} - {self.name}"
    
    def city(self):
        return self.region_id.city
    def gugoon(self):
        return self.region_id.gugoon
    
class CenterPhoto(models.Model):
    id = models.AutoField(primary_key=True)
    center = models.ForeignKey(Center, related_name='photos', on_delete=models.CASCADE, null=True, blank=True)
    image=models.ImageField(verbose_name="센터이미지",blank=True)
    
class Cart (BaseModel):
    id=models.AutoField(primary_key=True)
    center1=models.ForeignKey(Center,related_name='cart_center1', on_delete=models.CASCADE,blank=True, null=True)
    center2=models.ForeignKey(Center,related_name='cart_center2', on_delete=models.CASCADE,blank=True, null=True)
    center3=models.ForeignKey(Center,related_name='cart_center3', on_delete=models.CASCADE,blank=True, null=True)
    center4=models.ForeignKey(Center,related_name='cart_center4', on_delete=models.CASCADE,blank=True, null=True)
    center5=models.ForeignKey(Center,related_name='cart_center5', on_delete=models.CASCADE,blank=True, null=True)

    def total_cost(self):
        centers = [self.center1, self.center2, self.center3, self.center4, self.center5]
        total = sum(center.cost for center in centers if center is not None)
        return 4 * total
    # def total_cost(self):
    #     return 4*(self.center1.cost + self.center2.cost + self.center3.cost+self.center4.cost+self.center5.cost) #이용비용 계산 (한달 기준으로 계산해줌.)

    def __str__(self):
        return f"Cart with facilities: {self.center1}, {self.center2}, {self.center3},{self.center4},{self.center5}"

class CenterReview(BaseModel):
    id=models.AutoField(primary_key=True)
    center_id=models.ForeignKey(Center, verbose_name="시설",on_delete=models.CASCADE)
    user_id=models.ForeignKey(User, verbose_name="작성자", on_delete=models.CASCADE, null=True)
    content=models.CharField(verbose_name="후기내용", max_length=150) #일단은 150자 이내로 쓰게함
    score=models.IntegerField(verbose_name="별점",null=True, blank=True)
    thumbnail = models.ImageField(verbose_name="썸네일", null=True, blank=True)

class Report(BaseModel): #사용자 여가시설 리포트
    id=models.AutoField(primary_key=True)
    user_id=models.ForeignKey(User, verbose_name="작성자", on_delete=models.CASCADE)
    region_id=models.ForeignKey(Region, verbose_name="지역", on_delete=models.CASCADE, null=True)
    plan1=models.TextField(verbose_name="계획1", null=True)
    plan2=models.TextField(verbose_name="계획2", null=True)
    plan3=models.TextField(verbose_name="계획3", null=True)

    def city(self):
        return self.region_id.city
    def gugoon(self):
        return self.region_id.gugoon