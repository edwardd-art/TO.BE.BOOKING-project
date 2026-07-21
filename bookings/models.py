from django.db import models
from django.contrib.auth.models import User


class Table(models.Model):
    TABLE_TYPES = [
        ('small', 'Маленький (2 места)'),
        ('medium', 'Средний (4 места)'),
        ('large', 'Большой (6+ мест)'),
    ]

    number = models.IntegerField(unique=True, verbose_name="Номер столика")
    table_type = models.CharField(max_length=20, choices=TABLE_TYPES, default='medium')
    seats = models.IntegerField(verbose_name="Количество мест")
    description = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True, verbose_name="Доступен")
    pos_x = models.IntegerField(default=0)
    pos_y = models.IntegerField(default=0)

    def __str__(self):
        return f"Столик #{self.number} ({self.seats} мест)"

    class Meta:
        verbose_name = "Столик"
        verbose_name_plural = "Столики"


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает подтверждения'),
        ('confirmed', 'Подтверждено'),
        ('completed', 'Завершено'),
        ('cancelled', 'Отменено'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings', null=True, blank=True)
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='bookings')
    date = models.DateField(verbose_name="Дата")
    time_start = models.TimeField(verbose_name="Время начала")
    time_end = models.TimeField(verbose_name="Время окончания", null=True, blank=True)
    guests_count = models.IntegerField(verbose_name="Количество гостей")
    name = models.CharField(max_length=100, verbose_name="Имя")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    comment = models.TextField(blank=True, verbose_name="Комментарий")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Бронь #{self.id} - {self.table} - {self.date}"

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"
        ordering = ['-created_at']