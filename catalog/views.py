from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Avg, Count
from django.db.models.functions import Lower
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Category, Product, Review
from .forms import ReviewForm


def product_list(request, category_slug=None):
    category = None
    products = Product.objects.filter(available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    # === ПОИСК ===
    query = request.GET.get('q')
    if query:
        words = query.strip().split()
        products = products.annotate(
            name_lower=Lower('name'),
            desc_lower=Lower('description')
        )
        q_objects = Q()
        for word in words:
            word_lower = word.lower()
            q_objects |= Q(name_lower__contains=word_lower) | Q(desc_lower__contains=word_lower)
        products = products.filter(q_objects)

        category_q = Q()
        for word in words:
            category_q |= Q(category__name__icontains=word)
        category_products = Product.objects.filter(available=True).filter(category_q)
        products = (products | category_products).distinct()

    # === ФИЛЬТРАЦИЯ ===
    gender = request.GET.get('gender')
    if gender:
        products = products.filter(gender=gender)

    brand = request.GET.get('brand')
    if brand:
        products = products.filter(brand__iexact=brand)

    color = request.GET.get('color')
    if color:
        products = products.filter(color__icontains=color)

    price_min = request.GET.get('price_min')
    if price_min:
        try:
            products = products.filter(price__gte=float(price_min))
        except ValueError:
            pass

    price_max = request.GET.get('price_max')
    if price_max:
        try:
            products = products.filter(price__lte=float(price_max))
        except ValueError:
            pass

    # === СОРТИРОВКА ===
    sort = request.GET.get('sort')
    if sort == 'price':
        products = products.order_by('price')
    elif sort == '-price':
        products = products.order_by('-price')
    elif sort == 'name':
        products = products.order_by('name')
    else:
        products = products.order_by('-created')

    # === АННОТАЦИЯ РЕЙТИНГА И ОТЗЫВОВ ===
    products = products.annotate(
        avg_rating=Avg('reviews__rating'),
        reviews_count=Count('reviews')
    )

    # Для фильтра
    brands = Product.objects.filter(available=True).exclude(brand='').values_list('brand', flat=True).distinct()
    colors = Product.objects.filter(available=True).exclude(color='').values_list('color', flat=True).distinct()

    # === ПАГИНАЦИЯ ===
    paginator = Paginator(products, 6)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    categories = Category.objects.all()

    context = {
        'category': category,
        'products': products,
        'categories': categories,
        'query': query,
        'brands': brands,
        'colors': colors,
    }
    return render(request, 'catalog/product_list.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)

    # Средний рейтинг
    rating_data = product.reviews.aggregate(avg=Avg('rating'), count=Count('id'))
    avg_rating = rating_data['avg'] or 0
    reviews_count = rating_data['count']

    # Похожие товары
    similar_products = Product.objects.filter(
        category=product.category, available=True
    ).exclude(id=product.id)[:4]

    # Форма отзыва
    review_form = ReviewForm()

    # Проверяем, может ли пользователь оставить отзыв
    user_can_review = False
    user_review = None
    if request.user.is_authenticated:
        user_review = product.reviews.filter(user=request.user).first()
        user_can_review = user_review is None

    context = {
        'product': product,
        'similar_products': similar_products,
        'avg_rating': avg_rating,
        'reviews_count': reviews_count,
        'review_form': review_form,
        'user_can_review': user_can_review,
        'user_review': user_review,
    }
    return render(request, 'catalog/product_detail.html', context)


@login_required
def add_review(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)

    if product.reviews.filter(user=request.user).exists():
        messages.warning(request, 'Вы уже оставили отзыв на этот товар.')
        return redirect('catalog:product_detail', slug=slug)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, 'Спасибо за ваш отзыв!')
            return redirect('catalog:product_detail', slug=slug)
    else:
        form = ReviewForm()

    return render(request, 'catalog/add_review.html', {'form': form, 'product': product})


def about(request):
    return render(request, 'catalog/about.html')


def contacts(request):
    return render(request, 'catalog/contacts.html')