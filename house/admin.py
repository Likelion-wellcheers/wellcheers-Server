from django.contrib import admin
from .models import House_type , House, House_Surroundings, Infra, Mood, SilverTown, Region, SilverTown_Service

# Register your models here.
admin.site.register(House)
admin.site.register(House_type)
admin.site.register(House_Surroundings)
admin.site.register(Infra)
admin.site.register(Mood)
admin.site.register(SilverTown)
admin.site.register(SilverTown_Service)
admin.site.register(Region)