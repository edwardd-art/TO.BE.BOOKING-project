from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from bookings.models import Booking


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, 'Пароли не совпадают')
            return render(request, 'registration/register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Пользователь с таким именем уже существует')
            return render(request, 'registration/register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Пользователь с таким email уже существует')
            return render(request, 'registration/register.html')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )
        login(request, user)
        messages.success(request, 'Регистрация прошла успешно!')
        return redirect('/')

    return render(request, 'registration/register.html')


@login_required
def profile(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')

    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        action = request.POST.get('action')

        try:
            booking = Booking.objects.get(id=booking_id, user=request.user)

            if action == 'cancel':
                booking.status = 'cancelled'
                booking.save()
                messages.success(request, f'Бронирование #{booking.id} отменено')
                return redirect('users:profile')  # ← ЯВНЫЙ РЕДИРЕКТ

            elif action == 'edit':
                return redirect('users:edit_booking', booking_id=booking.id)

        except Booking.DoesNotExist:
            messages.error(request, 'Бронирование не найдено')
            return redirect('users:profile')

        # Если ничего не сработало — редирект
        return redirect('users:profile')

    return render(request, 'users/profile.html', {'bookings': bookings})


@login_required
def edit_booking(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id, user=request.user)

        if booking.status in ['completed', 'cancelled']:
            messages.error(request, 'Это бронирование нельзя изменить')
            return redirect('users:profile')

        if request.method == 'POST':
            date = request.POST.get('date')
            time = request.POST.get('time')
            guests = request.POST.get('guests')
            comment = request.POST.get('comment')

            existing_booking = Booking.objects.filter(
                table=booking.table,
                date=date,
                time_start=time,
                status__in=['pending', 'confirmed']
            ).exclude(id=booking.id).exists()

            if existing_booking:
                messages.error(request, 'Это время уже занято')
                return render(request, 'users/edit_booking.html', {'booking': booking})

            booking.date = date
            booking.time_start = time
            booking.guests_count = guests
            booking.comment = comment
            booking.save()

            messages.success(request, f'Бронирование #{booking.id} обновлено')
            return redirect('users:profile')

        return render(request, 'users/edit_booking.html', {'booking': booking})

    except Booking.DoesNotExist:
        messages.error(request, 'Бронирование не найдено')
        return redirect('users:profile')