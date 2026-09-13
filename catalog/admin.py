from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'description_preview')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')

    def description_preview(self, obj):
        return obj.description[:50] + '…' if len(obj.description) > 50 else obj.description
    description_preview.short_description = 'Описание (кратко)'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'category', 'brand', 'gender', 'price', 'available',
        'image_preview', 'created'
    )
    list_editable = ('price', 'available', 'brand', 'gender')
    list_filter = ('category', 'gender', 'available', 'created')
    search_fields = ('name', 'description', 'slug', 'brand', 'composition', 'color')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('-created',)
    date_hierarchy = 'created'
    fieldsets = (
        (None, {
            'fields': ('category', 'name', 'slug', 'description', 'price', 'image', 'available')
        }),
        ('Характеристики', {
            'fields': ('brand', 'composition', 'gender', 'color'),
            'classes': ('wide',),
        }),
        ('Дополнительно', {
            'classes': ('collapse',),
            'fields': ('created', 'updated'),
        }),
    )
    readonly_fields = ('created', 'updated')

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px; border-radius: 4px;" />', obj.image.url)
        return '-'
    image_preview.short_description = 'Изображение'

    actions = ['make_available', 'make_unavailable']

    def make_available(self, request, queryset):
        queryset.update(available=True)
    make_available.short_description = 'Сделать доступными'

    def make_unavailable(self, request, queryset):
        queryset.update(available=False)
    make_unavailable.short_description = 'Сделать недоступными'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating', 'created')
    list_filter = ('rating', 'created')
    search_fields = ('user__username', 'product__name', 'text')
    readonly_fields = ('created', 'updated')
    date_hierarchy = 'created'