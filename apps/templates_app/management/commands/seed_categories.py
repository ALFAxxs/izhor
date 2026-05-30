from django.core.management.base import BaseCommand
from apps.templates_app.models import Category

CATEGORIES = [
    ('Sevgi',         'sevgi',        '❤️',  0),
    ("Do'stlik",      'dostlik',      '🤝',  1),
    ('Ota-ona',       'ota-ona',      '👨‍👩‍👧', 2),
    ("Tug'ilgan kun", 'tugilgan-kun', '🎂',  3),
    ("To'y",          'toy',          '💍',  4),
    ('Bayram',        'bayram',       '🎉',  5),
    ('Surprise',      'surprise',     '🎁',  6),
    ('Anniversary',   'anniversary',  '🌹',  7),
    ('Uzr',           'uzr',          '🙏',  8),
    ('Motivatsiya',   'motivatsiya',  '⭐',  9),
]

class Command(BaseCommand):
    help = 'Kategoriyalarni seed qilish'

    def handle(self, *args, **options):
        for name, slug, icon, order in CATEGORIES:
            cat, created = Category.objects.get_or_create(
                slug=slug,
                defaults={'name': name, 'icon': icon, 'order': order}
            )
            self.stdout.write(f"{'Yaratildi' if created else 'Mavjud'}: {name}")
        self.stdout.write(self.style.SUCCESS('Kategoriyalar tayyor!'))
