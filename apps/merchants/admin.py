from django.contrib import admin
from .models import Merchant

@admin.register(Merchant)
class MerchantAdmin(admin.ModelAdmin):
    list_display  = ('shop_name', 'user', 'plan', 'is_active', 'qr_limit', 'created_at')
    list_filter   = ('plan', 'is_active')
    search_fields = ('shop_name', 'user__username')
    readonly_fields = ('created_at',)
