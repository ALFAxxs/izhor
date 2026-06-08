from django.db import models
from apps.merchants.models import Merchant


class Category(models.Model):
    name    = models.CharField(max_length=100)   # Sevgi, Do'stlik, Tug'ilgan kun ...
    slug    = models.SlugField(unique=True)
    icon    = models.CharField(max_length=50, blank=True)  # emoji yoki icon nomi
    order   = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class IzhorTemplate(models.Model):
    class Status(models.TextChoices):
        DRAFT     = 'draft',     'Qoralama'
        PUBLISHED = 'published', 'Nashr etilgan'

    merchant    = models.ForeignKey(Merchant, on_delete=models.CASCADE, related_name='templates')
    category    = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    title       = models.CharField(max_length=200)
    status      = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    view_count  = models.PositiveIntegerField(default=0)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} — {self.merchant.shop_name}"


class TemplateConfig(models.Model):
    """
    Shablon vizual konfiguratsiyasi JSON sifatida saqlanadi.
    Builder yuborgan barcha sozlamalar shu yerda.
    """
    template        = models.OneToOneField(IzhorTemplate, on_delete=models.CASCADE, related_name='config')

    # Background
    bg_type         = models.CharField(max_length=20, default='color')  # color | image | video | gradient
    bg_value        = models.TextField(blank=True)  # hex, url yoki gradient string
    bg_overlay      = models.FloatField(default=0.0)  # 0.0 - 1.0
    bg_blur         = models.PositiveSmallIntegerField(default=0)

    # Title
    title_text      = models.CharField(max_length=300, blank=True)
    title_font      = models.CharField(max_length=100, default='Playfair Display')
    title_size      = models.PositiveSmallIntegerField(default=42)
    title_color     = models.CharField(max_length=20, default='#ffffff')
    title_effect      = models.CharField(max_length=30, default='none')  # glow | typewriter | float | pulse | neon | shake
    title_font_effect = models.CharField(max_length=30, default='none')  # shadow | outline | gradient-pink | gradient-gold

    # Message
    message_text    = models.TextField(blank=True)
    message_font    = models.CharField(max_length=100, default='Crimson Pro')
    message_size    = models.PositiveSmallIntegerField(default=18)
    message_color   = models.CharField(max_length=20, default='#f0e0e8')

    # Decorations (JSON list)
    decorations     = models.JSONField(default=list)
    # Example: [{"type": "hearts", "speed": 1.0, "opacity": 0.7, "count": 20}]

    # Audio
    audio_file      = models.FileField(upload_to='audio/', blank=True, null=True)
    audio_autoplay  = models.BooleanField(default=False)
    audio_hidden    = models.BooleanField(default=False)  # faqat background

    updated_at      = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Config: {self.template.title}"


class AudioFile(models.Model):
    merchant    = models.ForeignKey(Merchant, on_delete=models.CASCADE, related_name='audio_files')
    name        = models.CharField(max_length=200)
    file        = models.FileField(upload_to='audio/')
    duration    = models.PositiveIntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class EventTemplate(models.Model):
    """To'y va osh taklifnomalari uchun model"""

    class EventType(models.TextChoices):
        WEDDING = 'wedding', "Nikoh to'yi"
        OSH     = 'osh',     'Osh marosimi'

    merchant        = models.ForeignKey(Merchant, on_delete=models.CASCADE, related_name='event_templates')
    event_type      = models.CharField(max_length=20, choices=EventType.choices)
    title           = models.CharField(max_length=200)
    status          = models.CharField(max_length=20, default='draft')
    view_count      = models.PositiveIntegerField(default=0)

    couple_names    = models.CharField(max_length=200, blank=True)
    invite_text     = models.TextField(blank=True)
    event_date      = models.DateTimeField(null=True, blank=True)
    venue_name      = models.CharField(max_length=200, blank=True)
    venue_address   = models.CharField(max_length=300, blank=True)
    map_url         = models.URLField(blank=True)
    audio_file      = models.FileField(upload_to='audio/', blank=True, null=True)
    audio_autoplay  = models.BooleanField(default=True)  # ochilganda avtomatik yangrasinmi

    meal_type       = models.CharField(max_length=50, blank=True, default='Ertalabki osh')

    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_event_type_display()} — {self.title}"
