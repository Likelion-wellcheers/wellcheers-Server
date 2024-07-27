from django.contrib import admin
from .models import Infra, Mood, Region, House_type
class RegionAdmin(admin.ModelAdmin):
    list_display = ('id', 'city', 'gu', 'goon', 'created_at')
    search_fields = ('city', 'gu', 'goon')
    list_filter = ('city', 'gu')
    filter_horizontal = ('htype_id', 'infra_id', 'mood_id')  # ManyToMany 필드를 위한 필터 사용

# Register your models here.
admin.site.register(Infra)
admin.site.register(Mood)
admin.site.register(Region, RegionAdmin)
admin.site.register(House_type)