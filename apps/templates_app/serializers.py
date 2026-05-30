from rest_framework import serializers
from .models import Category, IzhorTemplate, TemplateConfig, AudioFile


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model  = Category
        fields = ('id', 'name', 'slug', 'icon')


class TemplateConfigSerializer(serializers.ModelSerializer):
    audio_url = serializers.SerializerMethodField()

    class Meta:
        model  = TemplateConfig
        exclude = ('template',)

    def get_audio_url(self, obj):
        request = self.context.get('request')
        if obj.audio_file and request:
            return request.build_absolute_uri(obj.audio_file.url)
        return None


class TemplateListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    qr_slug       = serializers.CharField(source='qr_code.slug', read_only=True)

    class Meta:
        model  = IzhorTemplate
        fields = ('id', 'title', 'status', 'category_name', 'view_count', 'qr_slug', 'created_at')


class TemplateDetailSerializer(serializers.ModelSerializer):
    config        = TemplateConfigSerializer(read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    qr_slug       = serializers.CharField(source='qr_code.slug', read_only=True)
    qr_image_url  = serializers.SerializerMethodField()

    class Meta:
        model  = IzhorTemplate
        fields = ('id', 'title', 'status', 'category', 'category_name',
                  'view_count', 'qr_slug', 'qr_image_url', 'config', 'created_at', 'updated_at')

    def get_qr_image_url(self, obj):
        request = self.context.get('request')
        try:
            if obj.qr_code.qr_image and request:
                return request.build_absolute_uri(obj.qr_code.qr_image.url)
        except Exception:
            pass
        return None


class TemplateCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model  = IzhorTemplate
        fields = ('title', 'category')


class TemplateConfigUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model  = TemplateConfig
        exclude = ('template', 'updated_at')


class AudioFileSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model  = AudioFile
        fields = ('id', 'name', 'file', 'file_url', 'duration', 'uploaded_at')
        read_only_fields = ('uploaded_at',)

    def get_file_url(self, obj):
        request = self.context.get('request')
        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)
        return None