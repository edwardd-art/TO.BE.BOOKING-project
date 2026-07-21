from django.shortcuts import render
from .models import Service

def home_view(request):
    services = Service.objects.all()
    return render(request, 'core/home.html', {'services': services})

def about_view(request):
    return render(request, 'core/about.html')

def contacts_view(request):
    return render(request, 'core/contacts.html')