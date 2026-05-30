from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Category, IzhorTemplate, TemplateConfig, AudioFile
from .serializers import (
    CategorySerializer, TemplateListSerializer, TemplateDetailSerializer,
    TemplateCreateSerializer, TemplateConfigUpdateSerializer, AudioFileSerializer
)


def get_merchant(request):
    from apps.merchants.models import Merchant
    if hasattr(request.user, 'merchant'):
        return request.user.merchant
    merchant, _ = Merchant.objects.get_or_create(
        user=request.user,
        defaults={'shop_name': request.user.username, 'plan': Merchant.Plan.FREE}
    )
    return merchant


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def category_list(request):
    cats = Category.objects.all()
    return Response(CategorySerializer(cats, many=True).data)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def template_list(request):
    merchant = get_merchant(request)

    if request.method == 'GET':
        qs = IzhorTemplate.objects.filter(merchant=merchant).select_related('category', 'qr_code')
        category    = request.GET.get('category')
        tmpl_status = request.GET.get('status')
        if category:    qs = qs.filter(category__slug=category)
        if tmpl_status: qs = qs.filter(status=tmpl_status)
        return Response(TemplateListSerializer(qs, many=True).data)

    serializer = TemplateCreateSerializer(data=request.data)
    if serializer.is_valid():
        template = serializer.save(merchant=merchant)
        TemplateConfig.objects.create(template=template)
        _create_qr(template, request)
        return Response(
            TemplateDetailSerializer(template, context={'request': request}).data,
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def template_detail(request, pk):
    merchant = get_merchant(request)
    try:
        template = IzhorTemplate.objects.get(pk=pk, merchant=merchant)
    except IzhorTemplate.DoesNotExist:
        return Response({'error': 'Shablon topilmadi.'}, status=404)

    if request.method == 'GET':
        return Response(TemplateDetailSerializer(template, context={'request': request}).data)

    if request.method == 'PUT':
        if 'title' in request.data:    template.title = request.data['title']
        if 'status' in request.data:   template.status = request.data['status']
        if 'category' in request.data: template.category_id = request.data['category']
        template.save()
        return Response(TemplateDetailSerializer(template, context={'request': request}).data)

    template.delete()
    return Response(status=204)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def template_config_update(request, pk):
    merchant = get_merchant(request)
    try:
        template = IzhorTemplate.objects.get(pk=pk, merchant=merchant)
        config   = template.config
    except (IzhorTemplate.DoesNotExist, TemplateConfig.DoesNotExist):
        return Response({'error': 'Topilmadi.'}, status=404)

    data = request.data.copy()

    # audio_file_id kelsa — AudioFile modelidan fayl olamiz
    audio_id = data.pop('audio_file_id', None)
    if audio_id:
        try:
            audio_obj = AudioFile.objects.get(id=audio_id, merchant=merchant)
            # TemplateConfig.audio_file ga AudioFile.file ni bog'laymiz
            config.audio_file = audio_obj.file
            config.save(update_fields=['audio_file'])
        except AudioFile.DoesNotExist:
            pass

    serializer = TemplateConfigUpdateSerializer(config, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(TemplateDetailSerializer(template, context={'request': request}).data)
    return Response(serializer.errors, status=400)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def audio_list(request):
    merchant = get_merchant(request)

    if request.method == 'GET':
        files = AudioFile.objects.filter(merchant=merchant)
        return Response(AudioFileSerializer(files, many=True, context={'request': request}).data)

    serializer = AudioFileSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(merchant=merchant)
        return Response(AudioFileSerializer(
            serializer.instance, context={'request': request}
        ).data, status=201)
    return Response(serializer.errors, status=400)


def _create_qr(template, request):
    from apps.qr_system.models import QRCode
    from apps.qr_system.utils import make_unique_slug, generate_qr_image
    slug     = make_unique_slug()
    base_url = request.build_absolute_uri(f'/i/{slug}')
    qr_img   = generate_qr_image(base_url, slug)
    qr = QRCode(template=template, slug=slug)
    qr.qr_image.save(f'qr_{slug}.png', qr_img, save=False)
    qr.save()
    return qr