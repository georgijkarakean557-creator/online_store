from django.shortcuts import render, redirect
from django.http import JsonResponse
from cart.cart import Cart
from .models import Order, OrderItem, PickupPoint
from .forms import OrderCreateForm
from users.models import Address
from core.email_utils import send_order_confirmation_email
import json


def order_create(request):
    cart = Cart(request)
    if not cart:
        return redirect('cart:cart_detail')

    user_addresses = None
    if request.user.is_authenticated:
        user_addresses = Address.objects.filter(user=request.user)

    pickup_point_id = request.session.get('pickup_point_id')
    pickup_point = None
    if pickup_point_id:
        try:
            pickup_point = PickupPoint.objects.get(id=pickup_point_id, is_active=True)
        except PickupPoint.DoesNotExist:
            pass

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.total_price = cart.get_total_price()
            if request.user.is_authenticated:
                order.user = request.user
                address_id = request.POST.get('address_id')
                if address_id:
                    address = Address.objects.get(id=address_id, user=request.user)
                    order.address = f"{address.country}, {address.city}, {address.street} {address.house}"
                    if address.apartment:
                        order.address += f", кв.{address.apartment}"

            if pickup_point:
                order.pickup_point = pickup_point

            order.save()

            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )

            send_order_confirmation_email(order.email, order.id, order.total_price, order.first_name)

            cart.clear()
            if 'pickup_point_id' in request.session:
                del request.session['pickup_point_id']

            return render(request, 'orders/created.html', {'order': order})
    else:
        form = OrderCreateForm()

    return render(request, 'orders/create.html', {
        'form': form,
        'cart': cart,
        'user_addresses': user_addresses,
        'pickup_point': pickup_point,
    })


def pickup_point_map(request):
    """Страница выбора пункта выдачи с картой."""
    points = PickupPoint.objects.filter(is_active=True)

    # Уникальные значения через set (distinct() ломается из-за Meta.ordering)
    cities = sorted(set(points.values_list('city', flat=True)))
    carriers_set = set(points.values_list('carrier', flat=True))
    carriers = [(slug, name) for slug, name in PickupPoint.CARRIER_CHOICES if slug in carriers_set]

    points_data = [
        {
            'id': p.id,
            'carrier': p.get_carrier_display(),
            'carrier_slug': p.carrier,
            'carrier_color': p.carrier_color,
            'name': p.name,
            'address': p.address,
            'city': p.city,
            'lat': float(p.latitude),
            'lng': float(p.longitude),
            'phone': p.phone,
            'work_time': p.work_time,
        }
        for p in points
    ]

    return render(request, 'orders/pickup_map.html', {
        'points': points,
        'points_json': json.dumps(points_data, ensure_ascii=False),
        'cities': cities,
        'carriers': carriers,
    })


def set_pickup_point(request, point_id):
    """Сохраняет выбранный пункт в сессию."""
    try:
        point = PickupPoint.objects.get(id=point_id, is_active=True)
        request.session['pickup_point_id'] = point.id
        return JsonResponse({'status': 'ok', 'name': point.name, 'address': point.address})
    except PickupPoint.DoesNotExist:
        return JsonResponse({'status': 'error'}, status=404)