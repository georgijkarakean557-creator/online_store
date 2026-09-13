from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm, AddressForm
from .models import Profile, Address, ChatMessage
from orders.models import Order, PickupPoint
import re
import random
import json


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('users:profile')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    orders = Order.objects.filter(user=request.user).order_by('-created')
    return render(request, 'users/profile.html', {'orders': orders})


@login_required
def edit_profile(request):
    if not hasattr(request.user, 'profile'):
        Profile.objects.create(user=request.user)

    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = ProfileEditForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Профиль успешно обновлён!')
            return redirect('users:profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'users/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Пароль успешно изменён!')
            return redirect('users:profile')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/change_password.html', {'form': form})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'users/order_detail.html', {'order': order})


# ----- Управление адресами -----
@login_required
def address_list(request):
    addresses = Address.objects.filter(user=request.user)

    addresses_data = [
        {
            'id': a.id,
            'name': a.name or 'Адрес',
            'city': a.city,
            'street': a.street,
            'house': a.house,
            'apartment': a.apartment or '',
            'postal_code': a.postal_code or '',
            'is_default': a.is_default,
            'lat': float(a.latitude) if a.latitude else None,
            'lng': float(a.longitude) if a.longitude else None,
        }
        for a in addresses
    ]

    return render(request, 'users/address_list.html', {
        'addresses': addresses,
        'addresses_json': json.dumps(addresses_data, ensure_ascii=False),
    })


@login_required
def address_add(request):
    pickup_points = PickupPoint.objects.filter(is_active=True)
    points_data = [
        {
            'id': p.id,
            'carrier': p.get_carrier_display(),
            'carrier_slug': p.carrier,
            'name': p.name,
            'address': p.address,
            'city': p.city,
            'street': p.address.split(',')[0].strip() if p.address else '',
            'lat': float(p.latitude),
            'lng': float(p.longitude),
        }
        for p in pickup_points
    ]

    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            if address.is_default:
                Address.objects.filter(user=request.user, is_default=True).update(is_default=False)
            address.save()
            messages.success(request, 'Адрес добавлен!')
            return redirect('users:address_list')
    else:
        form = AddressForm()
    return render(request, 'users/address_form.html', {
        'form': form,
        'title': 'Добавление адреса',
        'points_json': json.dumps(points_data, ensure_ascii=False),
    })


@login_required
def address_edit(request, address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)

    pickup_points = PickupPoint.objects.filter(is_active=True)
    points_data = [
        {
            'id': p.id,
            'carrier': p.get_carrier_display(),
            'carrier_slug': p.carrier,
            'name': p.name,
            'address': p.address,
            'city': p.city,
            'street': p.address.split(',')[0].strip() if p.address else '',
            'lat': float(p.latitude),
            'lng': float(p.longitude),
        }
        for p in pickup_points
    ]

    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            address = form.save(commit=False)
            if address.is_default:
                Address.objects.filter(user=request.user, is_default=True).exclude(id=address.id).update(is_default=False)
            address.save()
            messages.success(request, 'Адрес обновлён!')
            return redirect('users:address_list')
    else:
        form = AddressForm(instance=address)
    return render(request, 'users/address_form.html', {
        'form': form,
        'title': 'Редактирование адреса',
        'points_json': json.dumps(points_data, ensure_ascii=False),
    })


@login_required
def address_delete(request, address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)
    if request.method == 'POST':
        address.delete()
        messages.success(request, 'Адрес удалён.')
        return redirect('users:address_list')
    return render(request, 'users/address_confirm_delete.html', {'address': address})


# ----- НАСТРОЙКИ -----
@login_required
def settings(request):
    return render(request, 'users/settings.html')


# ---------- ЧАТ С ПОДДЕРЖКОЙ ----------
@login_required
def chat(request):
    history = ChatMessage.objects.filter(user=request.user)

    if request.method == 'POST':
        message_text = request.POST.get('message', '').strip()
        if message_text:
            ChatMessage.objects.create(
                user=request.user,
                message=message_text,
                is_bot=False
            )
            bot_response = generate_bot_response(message_text)
            ChatMessage.objects.create(
                user=request.user,
                message=bot_response,
                is_bot=True
            )
            return redirect('users:chat')

    return render(request, 'users/chat.html', {'history': history})


def generate_bot_response(message):
    """Логика ответа бота."""
    msg = message.lower()

    responses = {
        r'привет|здравствуй|добрый день|доброе утро|добрый вечер':
            'Здравствуйте! Чем я могу вам помочь? Задайте вопрос о товарах, ценах, доставке или возврате.',
        r'цена|стоимость|сколько стоит|почём':
            'Все цены указаны на сайте в карточках товаров. Если не нашли нужный товар, напишите его название, и я помогу найти информацию.',
        r'доставка|отправка|привезут|курьер':
            'Мы доставляем по всей России. Сроки: 2–5 рабочих дней. Стоимость доставки рассчитывается автоматически при оформлении заказа.',
        r'возврат|обмен|вернуть':
            'Вы можете вернуть товар в течение 14 дней с момента получения. Подробные условия на странице "Возврат" внизу сайта.',
        r'скидка|акция|распродажа|промокод':
            'Актуальные акции и скидки всегда на главной странице. Подпишитесь на рассылку, чтобы первыми узнавать о новых предложениях!',
        r'как заказать|оформление заказа|купить':
            'Чтобы оформить заказ, добавьте товары в корзину, затем перейдите в корзину и нажмите "Оформить заказ". Следуйте инструкциям на экране.',
        r'оплата|как оплатить|карта|наличные':
            'Мы принимаем оплату банковскими картами, через Яндекс.Кассу и наличными при получении (для некоторых регионов).',
        r'гарантия|гарантийный срок':
            'На все товары действует гарантия 12 месяцев. Подробности уточняйте у менеджера.',
        r'спасибо|благодарю|отлично|супер':
            'Рады помочь! Обращайтесь, если возникнут ещё вопросы.',
        r'пока|до свидания|всего хорошего':
            'До свидания! Всегда рады видеть вас в нашем магазине.'
    }

    for pattern, response in responses.items():
        if re.search(pattern, msg):
            return response

    default_responses = [
        'Спасибо за ваш вопрос! Наш специалист свяжется с вами в ближайшее время. А пока вы можете уточнить информацию о ценах, доставке или возврате.',
        'Интересный вопрос! Чтобы получить точный ответ, обратитесь к нашему менеджеру. Но я могу подсказать по основным темам: цены, доставка, возврат.',
        'Я ещё учусь, но постараюсь помочь. Попробуйте спросить о ценах, доставке или возврате товара.'
    ]
    return random.choice(default_responses)