from django.contrib import admin
from .models import Infra, Hobby, Region, Lifestyle, Center, CenterReview, Cart, Report

class RegionAdmin(admin.ModelAdmin):
    list_display = ('id', 'city', 'gugoon', 'created_at')
    search_fields = ('city', 'gugoon')
    list_filter = ('city', 'gugoon')
    filter_horizontal = ('lstyle_id', 'infra_id', 'hobby_id')  # ManyToMany 필드를 위한 필터 사용

# Register your models here.
admin.site.register(Infra)
admin.site.register(Hobby)
admin.site.register(Region, RegionAdmin)
admin.site.register(Lifestyle)
admin.site.register(Center)
admin.site.register(CenterReview)
admin.site.register(Cart)
admin.site.register(Report)