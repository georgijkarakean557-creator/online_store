from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import WishlistItem
from catalog.models import Product


@login_required
def wishlist_detail(request):
    """Страница избранного"""
    items = WishlistItem.objects.filter(user=request.user).select_related('product')
    return render(request, 'wishlist/wishlist_detail.html', {'items': items})


@login_required
def wishlist_add(request, product_id):
    """Добавление товара в избранное"""
    product = get_object_or_404(Product, id=product_id, available=True)
    # Проверяем, есть ли уже в избранном
    obj, created = WishlistItem.objects.get_or_create(user=request.user, product=product)
    if created:
        messages.success(request, f'Товар "{product.name}" добавлен в избранное.')
    else:
        messages.info(request, f'Товар "{product.name}" уже в избранном.')
    # Перенаправляем на страницу, с которой пришли, или в каталог
    next_url = request.META.get('HTTP_REFERER', 'catalog:product_list')
    return redirect(next_url)


@login_required
def wishlist_remove(request, product_id):
    """Удаление товара из избранного"""
    product = get_object_or_404(Product, id=product_id)
    item = WishlistItem.objects.filter(user=request.user, product=product).first()
    if item:
        item.delete()
        messages.success(request, f'Товар "{product.name}" удалён из избранного.')
    else:
        messages.warning(request, 'Товар не найден в избранном.')
    next_url = request.META.get('HTTP_REFERER', 'catalog:product_list')
    return redirect(next_url)