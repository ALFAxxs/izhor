import json
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from apps.qr_system.models import QRCode, ScanLog, EventQRCode


def _detect_device(ua):
    ua = ua.lower()
    if any(x in ua for x in ('iphone', 'android', 'mobile')):
        return 'mobile'
    if any(x in ua for x in ('ipad', 'tablet')):
        return 'tablet'
    return 'desktop'


def viewer(request, slug):
    qr = get_object_or_404(QRCode, slug=slug, is_active=True)
    if qr.expires_at and qr.expires_at < timezone.now():
        return render(request, 'viewer/expired.html')

    template = qr.template
    config   = getattr(template, 'config', None)

    ScanLog.objects.create(
        qr_code     = qr,
        ip_address  = request.META.get('REMOTE_ADDR'),
        user_agent  = request.META.get('HTTP_USER_AGENT', ''),
        device_type = _detect_device(request.META.get('HTTP_USER_AGENT', '')),
    )
    template.view_count += 1
    template.save(update_fields=['view_count'])

    return render(request, 'viewer/page.html', {
        'template':         template,
        'config':           config,
        'merchant':         template.merchant,
        'decorations_json': json.dumps(config.decorations if config else []),
    })


def event_viewer(request, slug):
    qr = get_object_or_404(EventQRCode, slug=slug, is_active=True)
    if qr.expires_at and qr.expires_at < timezone.now():
        return render(request, 'viewer/expired.html')

    event = qr.event_template
    event.view_count += 1
    event.save(update_fields=['view_count'])

    template_name = (
        'viewer/wedding.html' if event.event_type == 'wedding'
        else 'viewer/osh.html'
    )
    return render(request, template_name, {
        'event':    event,
        'merchant': event.merchant,
    })
