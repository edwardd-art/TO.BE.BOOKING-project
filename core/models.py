from django.db import models


class RestaurantInfo(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    address = models.CharField(max_length=300, verbose_name="Адрес")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    email = models.EmailField(verbose_name="Email")
    working_hours = models.TextField(verbose_name="Часы работы")
    logo = models.ImageField(upload_to='restaurant/', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Информация о ресторане"
        verbose_name_plural = "Информация о ресторане"


class Service(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    icon = models.CharField(max_length=50, verbose_name="Иконка")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order']
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"