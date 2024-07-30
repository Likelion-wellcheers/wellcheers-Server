from django.db import models
from house.models import Region
from accounts.models import User

# Create your models here.
class BaseModel(models.Model):
    created_at= models.DateTimeField(verbose_name="등록일시", auto_now_add=True)

    class Meta:
        abstract = True

class Question(BaseModel):
    id = models.AutoField(primary_key=True)
    q_user_id = models.ForeignKey(User, verbose_name="작성자", on_delete=models.CASCADE)
    region_id = models.ForeignKey(Region, verbose_name="지역", on_delete=models.CASCADE)
    title = models.CharField(verbose_name="제목", max_length=30)
    content = models.TextField(verbose_name="내용",  blank=True)
    image = models.ImageField(verbose_name="이미지", null=True, blank=True)
    finish = models.BooleanField(verbose_name="질문 해결 여부")

class Answer(BaseModel):
    id = models.AutoField(primary_key=True)
    q_id = models.ForeignKey(Question, verbose_name="질문글", on_delete=models.CASCADE)
    a_user_id = models.ForeignKey(User, verbose_name="답변자", on_delete=models.CASCADE)
    content = models.TextField(verbose_name="내용",  blank=True)