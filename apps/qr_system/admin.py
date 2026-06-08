from django.contrib import admin
from django.utils.html import format_html
from .models import QRCode, ScanLog


class ScanLogInline(admin.TabularInline):
    model   = ScanLog
    extra   = 0
    readonly_fields = ('ip_address', 'device_type', 'country', 'city', 'scanned_at')
    can_delete = False


@admin.register(QRCode)
class QRCodeAdmin(admin.ModelAdmin):
    list_display   = ('slug', 'template', 'is_active', 'scan_count', 'qr_preview', 'created_at')
    list_filter    = ('is_active',)
    readonly_fields = ('slug', 'qr_image', 'created_at', 'qr_preview')
    inlines        = [ScanLogInline]

    def scan_count(self, obj):
        return obj.scans.count()
    scan_count.short_description = "Skanlar"

    def qr_preview(self, obj):
        if obj.qr_image:
            return format_html('<img src="{}" width="80"/>', obj.qr_image.url)
        return "—"
    qr_preview.short_description = "QR"


@admin.register(ScanLog)
class ScanLogAdmin(admin.ModelAdmin):
    list_display  = ('qr_code', 'device_type', 'country', 'city', 'ip_address', 'scanned_at')
    list_filter   = ('device_type', 'country')
    readonly_fields = ('scanned_at',)


from .models import EventQRCode

@admin.register(EventQRCode)
class EventQRCodeAdmin(admin.ModelAdmin):
    list_display    = ('slug', 'event_template', 'is_active', 'created_at')
    readonly_fields = ('slug', 'qr_image', 'created_at')
