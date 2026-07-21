from django.contrib import admin
from .models import Table, Booking

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ['number', 'table_type', 'seats', 'is_active']
    list_filter = ['table_type', 'is_active']
    search_fields = ['number', 'description']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'table', 'date', 'time_start', 'user', 'status']
    list_filter = ['status', 'date']
    search_fields = ['name', 'phone']