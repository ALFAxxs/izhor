from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import HttpResponse
from .models import QRCode, ScanLog


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def qr_detail(request, pk):
    """Shablon QR ma'lumotlarini qaytarish"""
    try:
        qr = QRCode.objects.get(template__pk=pk, template__merchant__user=request.user)
    except QRCode.DoesNotExist:
        return Response({'error': 'QR topilmadi.'}, status=404)

    scans = qr.scans.all()
    device_stats = {}
    for s in scans:
        device_stats[s.device_type or 'unknown'] = device_stats.get(s.device_type or 'unknown', 0) + 1

    return Response({
        'slug':       qr.slug,
        'public_url': request.build_absolute_uri(f'/i/{qr.slug}'),
        'qr_image':   request.build_absolute_uri(qr.qr_image.url) if qr.qr_image else None,
        'is_active':  qr.is_active,
        'total_scans': scans.count(),
        'device_stats': device_stats,
        'created_at': qr.created_at,
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def qr_download(request, slug):
    """QR rasmini to'g'ridan-to'g'ri yuklab olish"""
    try:
        qr = QRCode.objects.get(slug=slug, template__merchant__user=request.user)
    except QRCode.DoesNotExist:
        return Response({'error': 'Topilmadi.'}, status=404)

    if not qr.qr_image:
        return Response({'error': 'QR rasm mavjud emas.'}, status=404)

    with qr.qr_image.open('rb') as f:
        response = HttpResponse(f.read(), content_type='image/png')
        response['Content-Disposition'] = f'attachment; filename="qr_{slug}.png"'
        return response


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def merchant_analytics(request):
    """Merchant uchun umumiy analytics"""
    merchant = getattr(request.user, 'merchant', None)
    if not merchant:
        return Response({'error': 'Merchant topilmadi.'}, status=404)

    from apps.templates_app.models import IzhorTemplate
    templates = IzhorTemplate.objects.filter(merchant=merchant)
    total_scans = ScanLog.objects.filter(qr_code__template__merchant=merchant).count()

    return Response({
        'total_templates': templates.count(),
        'published':       templates.filter(status='published').count(),
        'total_scans':     total_scans,
        'total_views':     sum(t.view_count for t in templates),
        'qr_limit':        merchant.qr_limit,
        'plan':            merchant.plan,
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def event_qr_download(request, slug):
    from .models import EventQRCode
    try:
        qr = EventQRCode.objects.get(slug=slug, event_template__merchant__user=request.user)
    except EventQRCode.DoesNotExist:
        return Response({'error': 'Topilmadi.'}, status=404)
    if not qr.qr_image:
        return Response({'error': 'QR rasm yo\'q.'}, status=404)
    with qr.qr_image.open('rb') as f:
        resp = HttpResponse(f.read(), content_type='image/png')
        resp['Content-Disposition'] = f'attachment; filename="qr_{slug}.png"'
        return resp
