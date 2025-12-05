from django.contrib import admin
from .models import ResourceType, WaterType, Object
# Register your models here.

admin.site.register(ResourceType)
admin.site.register(WaterType)
admin.site.register(Object)
