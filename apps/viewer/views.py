import json
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from apps.qr_system.models import QRCode, ScanLog


def _detect_device(user_agent: str) -> str:
    ua = user_agent.lower()
    if any(x in ua for x in ('iphone', 'android', 'mobile')):
        return 'mobile'
    if any(x in ua for x in ('ipad', 'tablet')):
        return 'tablet'
    return 'desktop'


def viewer(request, slug):
    qr = get_object_or_404(QRCode, slug=slug, is_active=True)

    # Muddati o'tgan bo'lsa
    if qr.expires_at and qr.expires_at < timezone.now():
        return render(request, 'viewer/expired.html')

    template = qr.template
    config   = getattr(template, 'config', None)

    # Scan log yozish
    ScanLog.objects.create(
        qr_code    = qr,
        ip_address = request.META.get('REMOTE_ADDR'),
        user_agent = request.META.get('HTTP_USER_AGENT', ''),
        device_type = _detect_device(request.META.get('HTTP_USER_AGENT', '')),
    )

    # View count oshirish
    template.view_count += 1
    template.save(update_fields=['view_count'])

    return render(request, 'viewer/page.html', {
        'template':        template,
        'config':          config,
        'merchant':        template.merchant,
        'decorations_json': json.dumps(config.decorations if config else []),
    })
