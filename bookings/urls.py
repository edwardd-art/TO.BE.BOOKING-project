from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('', views.booking_view, name='booking'),
    path('check-availability/', views.check_availability, name='check_availability'),
    path('confirmation/<int:booking_id>/', views.confirmation_view, name='confirmation'),
]