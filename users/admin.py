from django.contrib import admin
from django.utils.html import format_html
from .models import Profile, Address, ChatMessage


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'avatar_preview')
    search_fields = ('user__username', 'user__email', 'phone')

    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px; border-radius: 50%;" />', obj.avatar.url)
        return '-'
    avatar_preview.short_description = 'Аватар'


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'city', 'street', 'house', 'is_default')
    list_filter = ('city', 'is_default')
    search_fields = ('user__username', 'city', 'street')
    fieldsets = (
        (None, {'fields': ('user', 'name', 'is_default')}),
        ('Адрес', {'fields': ('country', 'city', 'street', 'house', 'apartment', 'postal_code')}),
        ('Координаты', {
            'fields': ('latitude', 'longitude'),
            'description': 'Скопируйте координаты с Яндекс.Карт: правый клик → «Что здесь?»'
        }),
    )


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'message_preview', 'is_bot', 'created_at')
    list_filter = ('is_bot', 'created_at')
    search_fields = ('user__username', 'message')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)

    def message_preview(self, obj):
        return obj.message[:50] + '…' if len(obj.message) > 50 else obj.message
    message_preview.short_description = 'Сообщение'