from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display  = ('username', 'email', 'role', 'phone', 'is_active', 'created_at')
    list_filter   = ('role', 'is_active')
    search_fields = ('username', 'email', 'phone')
    fieldsets     = UserAdmin.fieldsets + (
        ('Qo\'shimcha', {'fields': ('role', 'phone')}),
    )
