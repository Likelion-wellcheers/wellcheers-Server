from django.contrib import admin
from .models import Article, Magazine, Review, MagazinePhoto

# Register your models here.
admin.site.register(Article) #관리자 페이지에 모델추가
admin.site.register(Magazine)
admin.site.register(Review)
admin.site.register(MagazinePhoto)
# Register your models here.
