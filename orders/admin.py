from django.contrib import admin
from django.utils.html import format_html
from .models import Order, OrderItem, PickupPoint


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ('product',)
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'phone', 'total_price', 'paid', 'pickup_point', 'created')
    list_filter = ('paid', 'created', 'city')
    search_fields = ('first_name', 'last_name', 'email', 'phone', 'address')
    readonly_fields = ('created', 'updated', 'total_price')
    inlines = [OrderItemInline]
    fieldsets = (
        (None, {
            'fields': ('user', 'first_name', 'last_name', 'email', 'phone', 'address', 'city', 'postal_code', 'pickup_point')
        }),
        ('Финансы', {
            'fields': ('total_price', 'paid'),
        }),
        ('Время', {
            'fields': ('created', 'updated'),
            'classes': ('collapse',),
        }),
    )
    actions = ['mark_as_paid', 'mark_as_unpaid']

    def mark_as_paid(self, request, queryset):
        queryset.update(paid=True)
    mark_as_paid.short_description = 'Отметить как оплаченные'

    def mark_as_unpaid(self, request, queryset):
        queryset.update(paid=False)
    mark_as_unpaid.short_description = 'Отметить как неоплаченные'


@admin.register(PickupPoint)
class PickupPointAdmin(admin.ModelAdmin):
    list_display = ('carrier', 'name', 'city', 'address', 'is_active', 'map_preview')
    list_filter = ('carrier', 'city', 'is_active')
    search_fields = ('name', 'address', 'city')
    list_editable = ('is_active',)
    fieldsets = (
        (None, {
            'fields': ('carrier', 'name', 'is_active')
        }),
        ('Адрес', {
            'fields': ('city', 'address', 'phone', 'work_time')
        }),
        ('Координаты (для карты)', {
            'fields': ('latitude', 'longitude'),
            'description': 'Скопируйте координаты из Яндекс.Карт: найдите адрес → правый клик → "Что здесь?" → скопируйте широту и долготу.'
        }),
    )

    def map_preview(self, obj):
        return format_html(
            '<a href="https://yandex.ru/maps/?pt={},{}&z=17&l=map" target="_blank">Открыть на карте</a>',
            obj.longitude, obj.latitude
        )
    map_preview.short_description = 'На карте'