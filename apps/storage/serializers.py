from rest_framework import serializers
from .models import StorageConfig, MediaFile


class StorageConfigSerializer(serializers.ModelSerializer):
    """存储配置序列化器"""
    
    storage_type_display = serializers.CharField(source='get_storage_type_display', read_only=True)
    media_count = serializers.SerializerMethodField()
    
    class Meta:
        model = StorageConfig
        fields = ['id', 'name', 'storage_type', 'storage_type_display', 'is_active', 
                 'bucket_name', 'access_url', 'max_file_size', 'allowed_extensions',
                 'use_date_path', 'description', 'media_count', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
    
    def get_media_count(self, obj):
        """获取媒体文件数量"""
        return obj.media_files.count()


class MediaFileSerializer(serializers.ModelSerializer):
    """媒体文件序列化器"""
    
    file_type_display = serializers.CharField(source='get_file_type_display', read_only=True)
    file_size_mb = serializers.FloatField(read_only=True)
    storage_config_name = serializers.CharField(source='storage_config.name', read_only=True)
    uploaded_by_username = serializers.CharField(source='uploaded_by.username', read_only=True)
    
    class Meta:
        model = MediaFile
        fields = ['id', 'file_name', 'file_type', 'file_type_display', 'file_size', 'file_size_mb',
                 'storage_config', 'storage_config_name', 'storage_path', 'access_url',
                 'uploaded_by', 'uploaded_by_username', 'description', 'uploaded_at', 'updated_at']
        read_only_fields = ['uploaded_at', 'updated_at', 'access_url', 'storage_path']


class MediaFileUploadSerializer(serializers.ModelSerializer):
    """媒体文件上传序列化器"""
    
    class Meta:
        model = MediaFile
        fields = ['file_name', 'file_type', 'description']
