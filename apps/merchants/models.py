from django.db import models
from apps.accounts.models import User


class Merchant(models.Model):
    class Plan(models.TextChoices):
        FREE     = 'free',     'Bepul'
        BASIC    = 'basic',    'Basic'
        PREMIUM  = 'premium',  'Premium'
        BUSINESS = 'business', 'Business'

    user        = models.OneToOneField(User, on_delete=models.CASCADE, related_name='merchant')
    shop_name   = models.CharField(max_length=200)
    shop_logo   = models.ImageField(upload_to='logos/', blank=True, null=True)
    website     = models.URLField(blank=True)
    plan        = models.CharField(max_length=20, choices=Plan.choices, default=Plan.FREE)
    is_active   = models.BooleanField(default=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    # Limitlar
    @property
    def qr_limit(self):
        limits = {'free': 5, 'basic': 20, 'premium': 100, 'business': 9999}
        return limits.get(self.plan, 5)

    def __str__(self):
        return f"{self.shop_name} [{self.plan}]"
