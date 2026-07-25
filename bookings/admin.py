from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path
from .models import Table, Booking

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ['number', 'table_type', 'seats', 'is_active']
    list_filter = ['table_type', 'is_active']
    search_fields = ['number', 'description']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'table', 'date', 'time_start', 'user', 'name', 'phone', 'status', 'created_at']
    list_filter = ['status', 'date']
    search_fields = ['name', 'phone', 'table__number']
    readonly_fields = ['created_at']
    list_editable = ['status']  # ← ПОЗВОЛЯЕТ МЕНЯТЬ СТАТУС ПРЯМО В СПИСКЕ

    actions = ['confirm_bookings', 'cancel_bookings']  # ← МАССОВЫЕ ДЕЙСТВИЯ

    def confirm_bookings(self, request, queryset):
        """Подтвердить выбранные бронирования"""
        updated = queryset.update(status='confirmed')
        self.message_user(request, f'Подтверждено бронирований: {updated}')
    confirm_bookings.short_description = "Подтвердить выбранные бронирования"

    def cancel_bookings(self, request, queryset):
        """Отменить выбранные бронирования"""
        updated = queryset.update(status='cancelled')
        self.message_user(request, f'Отменено бронирований: {updated}')
    cancel_bookings.short_description = "Отменить выбранные бронирования"