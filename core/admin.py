from django.contrib import admin
from .models import RestaurantInfo, Service

@admin.register(RestaurantInfo)
class RestaurantInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email']

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'order']
    list_editable = ['order']