from django.contrib import admin
from .models import Article, Magazine, Review

# Register your models here.
admin.site.register(Article) #관리자 페이지에 모델추가
admin.site.register(Magazine)
admin.site.register(Review)
# Register your models here.
