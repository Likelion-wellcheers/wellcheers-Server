from django.contrib import admin
from .models import Infra, Mood, Region, House_type

# Register your models here.
admin.site.register(Infra)
admin.site.register(Mood)
admin.site.register(Region)
admin.site.register(House_type)