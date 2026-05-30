import uuid
from django.db import models
from apps.templates_app.models import IzhorTemplate


class QRCode(models.Model):
    template    = models.OneToOneField(IzhorTemplate, on_delete=models.CASCADE, related_name='qr_code')
    slug        = models.CharField(max_length=12, unique=True, db_index=True)
    qr_image    = models.ImageField(upload_to='qrcodes/', blank=True, null=True)
    is_active   = models.BooleanField(default=True)
    expires_at  = models.DateTimeField(blank=True, null=True)  # None = abadiy
    created_at  = models.DateTimeField(auto_now_add=True)

    def get_public_url(self):
        return f"/i/{self.slug}"

    def __str__(self):
        return f"QR: {self.slug} → {self.template.title}"


class ScanLog(models.Model):
    qr_code     = models.ForeignKey(QRCode, on_delete=models.CASCADE, related_name='scans')
    ip_address  = models.GenericIPAddressField(blank=True, null=True)
    user_agent  = models.TextField(blank=True)
    device_type = models.CharField(max_length=20, blank=True)  # mobile | tablet | desktop
    country     = models.CharField(max_length=100, blank=True)
    city        = models.CharField(max_length=100, blank=True)
    scanned_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-scanned_at']

    def __str__(self):
        return f"{self.qr_code.slug} @ {self.scanned_at:%Y-%m-%d %H:%M}"
