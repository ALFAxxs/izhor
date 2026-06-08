from django.contrib import admin
from .models import Category, IzhorTemplate, TemplateConfig, AudioFile


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display  = ('name', 'slug', 'icon', 'order')
    prepopulated_fields = {'slug': ('name',)}


class TemplateConfigInline(admin.StackedInline):
    model  = TemplateConfig
    extra  = 0


@admin.register(IzhorTemplate)
class IzhorTemplateAdmin(admin.ModelAdmin):
    list_display   = ('title', 'merchant', 'category', 'status', 'view_count', 'created_at')
    list_filter    = ('status', 'category')
    search_fields  = ('title', 'merchant__shop_name')
    readonly_fields = ('view_count', 'created_at', 'updated_at')
    inlines        = [TemplateConfigInline]


@admin.register(AudioFile)
class AudioFileAdmin(admin.ModelAdmin):
    list_display = ('name', 'merchant', 'duration', 'uploaded_at')


from .models import EventTemplate

@admin.register(EventTemplate)
class EventTemplateAdmin(admin.ModelAdmin):
    list_display    = ('title', 'event_type', 'merchant', 'status', 'event_date', 'view_count')
    list_filter     = ('event_type', 'status')
    search_fields   = ('title', 'merchant__shop_name', 'couple_names')
    readonly_fields = ('view_count', 'created_at', 'updated_at')
