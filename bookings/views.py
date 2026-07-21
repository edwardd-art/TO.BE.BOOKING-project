from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from .models import Table, Booking
from datetime import datetime


def booking_view(request):
    tables = Table.objects.filter(is_active=True)

    if request.method == 'POST':
        date = request.POST.get('date')
        time = request.POST.get('time')
        guests = request.POST.get('guests')
        table_id = request.POST.get('table_id')
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        comment = request.POST.get('comment', '')

        if not all([date, time, guests, table_id, name, phone]):
            messages.error(request, 'Заполните все поля')
            return render(request, 'bookings/booking.html', {'tables': tables})

        try:
            table = Table.objects.get(id=table_id)

            # Проверяем, свободен ли столик на выбранное время
            existing_booking = Booking.objects.filter(
                table=table,
                date=date,
                time_start=time,
                status__in=['pending', 'confirmed']
            ).exists()

            if existing_booking:
                messages.error(request, f'Столик #{table.number} уже занят на это время')
                return render(request, 'bookings/booking.html', {'tables': tables})

            user = request.user if request.user.is_authenticated else None

            Booking.objects.create(
                user=user,
                table=table,
                date=date,
                time_start=time,
                guests_count=guests,
                name=name,
                phone=phone,
                comment=comment,
                status='pending'
            )

            messages.success(request, f'Столик #{table.number} успешно забронирован!')
            return redirect('bookings:confirmation', booking_id=booking.id)

        except Table.DoesNotExist:
            messages.error(request, 'Столик не найден')
        except Exception as e:
            messages.error(request, f'Ошибка: {str(e)}')

    return render(request, 'bookings/booking.html', {'tables': tables})


def check_availability(request):
    """API для проверки доступности столиков (AJAX)"""
    if request.method == 'GET':
        date = request.GET.get('date')
        time = request.GET.get('time')
        table_id = request.GET.get('table_id')

        try:
            table = Table.objects.get(id=table_id)
            is_available = not Booking.objects.filter(
                table=table,
                date=date,
                time_start=time,
                status__in=['pending', 'confirmed']
            ).exists()

            return JsonResponse({
                'available': is_available,
                'message': 'Свободен' if is_available else 'Занят'
            })
        except Table.DoesNotExist:
            return JsonResponse({'error': 'Столик не найден'}, status=404)

    return JsonResponse({'error': 'Метод не разрешен'}, status=405)

def confirmation_view(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id)
        return render(request, 'bookings/confirmation.html', {'booking': booking})
    except Booking.DoesNotExist:
        messages.error(request, 'Бронирование не найдено')
        return redirect('home')