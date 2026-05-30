import random
import string
import qrcode
import qrcode.image.svg
from io import BytesIO
from django.core.files.base import ContentFile
from PIL import Image


def generate_slug(length=8):
    """Unique qisqa slug yaratish: abc12xyz"""
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choices(chars, k=length))


def make_unique_slug():
    from apps.qr_system.models import QRCode
    while True:
        slug = generate_slug()
        if not QRCode.objects.filter(slug=slug).exists():
            return slug


def generate_qr_image(url: str, slug: str) -> ContentFile:
    """
    URL dan QR code rasmi yaratish va ContentFile qaytarish.
    Strawberry House uchun: pushti rangda.
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="#c2185b", back_color="white")  # pushti rang

    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)

    return ContentFile(buffer.read(), name=f"qr_{slug}.png")
