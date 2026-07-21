from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Feedback

def feedback_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if not all([name, email, subject, message]):
            messages.error(request, 'Заполните все поля')
            return redirect('home')

        Feedback.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        messages.success(request, 'Ваше сообщение отправлено! Спасибо!')
        return redirect('home')

    return redirect('home')