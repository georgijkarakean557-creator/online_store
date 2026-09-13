from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from catalog.models import Product
from .cart import Cart


@login_required
@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id, available=True)
    quantity = int(request.POST.get('quantity', 1))
    cart.add(product=product, quantity=quantity, override_quantity=False)
    return redirect('cart:cart_detail')


@login_required
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


@login_required
def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})


@login_required
@require_POST
def cart_update(request, product_id):
    """Обновляет количество товара. Если quantity=0 — удаляет."""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id, available=True)
    quantity = int(request.POST.get('quantity', 1))
    if quantity > 0:
        cart.add(product=product, quantity=quantity, override_quantity=True)
    else:
        cart.remove(product)
    return redirect('cart:cart_detail')


@login_required
@require_POST
def cart_checkout_selected(request):
    """Оформление только выбранных товаров. Невыбранные — удаляются из корзины."""
    cart = Cart(request)
    selected_ids = request.POST.getlist('selected_ids')

    if not selected_ids:
        return redirect('cart:cart_detail')

    all_ids = list(cart.cart.keys())

    # Если выбраны все — сразу к оформлению
    if set(selected_ids) == set(all_ids):
        return redirect('orders:order_create')

    # Удаляем невыбранные
    for pid in all_ids:
        if pid not in selected_ids:
            del cart.cart[pid]
    cart.save()

    return redirect('orders:order_create')