from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('edit/<int:booking_id>/', views.edit_booking, name='edit_booking'),
]