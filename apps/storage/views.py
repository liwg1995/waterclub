from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.files.storage import default_storage
from django.utils.text import slugify
from django.utils import timezone
from datetime import datetime
import os
from .models import StorageConfig, MediaFile
from .serializers import StorageConfigSerializer, MediaFileSerializer, MediaFileUploadSerializer
from .storage_backends import get_storage_backend


class StorageConfigViewSet(viewsets.ModelViewSet):
    """存储配置API"""
    
    queryset = StorageConfig.objects.all()
    serializer_class = StorageConfigSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """获取当前激活的存储配置"""
        config = StorageConfig.objects.filter(is_active=True).first()
        if config:
            serializer = self.get_serializer(config)
            return Response(serializer.data)
        return Response({'detail': '没有激活的存储配置'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """激活指定的存储配置"""
        config = self.get_object()
        StorageConfig.objects.exclude(pk=pk).update(is_active=False)
        config.is_active = True
        config.save()
        serializer = self.get_serializer(config)
        return Response(serializer.data)


class MediaFileViewSet(viewsets.ModelViewSet):
    """媒体文件API"""
    
    queryset = MediaFile.objects.all()
    serializer_class = MediaFileSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['file_type', 'storage_config']
    search_fields = ['file_name', 'storage_path']
    ordering_fields = ['uploaded_at', 'file_size']
    ordering = ['-uploaded_at']
    
    def get_serializer_class(self):
        """根据操作获取不同的序列化器"""
        if self.action == 'create':
            return MediaFileUploadSerializer
        return MediaFileSerializer
    
    @action(detail=False, methods=['post'])
    def upload(self, request):
        """上传媒体文件"""
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({'detail': '请选择要上传的文件'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 获取当前激活的存储配置
        config = StorageConfig.objects.filter(is_active=True).first()
        if not config:
            return Response({'detail': '没有激活的存储配置'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # 获取存储后端
            backend = get_storage_backend(config)
            
            # 验证文件
            validation_error = backend.validate_file(file_obj)
            if validation_error:
                return Response({'detail': validation_error}, status=status.HTTP_400_BAD_REQUEST)
            
            # 上传文件
            storage_path, access_url = backend.upload_file(file_obj)
            
            # 确定文件类型
            file_type = self._get_file_type(file_obj.content_type, file_obj.name)
            
            # 创建媒体文件记录
            media_file = MediaFile.objects.create(
                file_name=file_obj.name,
                file_type=file_type,
                file_size=file_obj.size,
                storage_config=config,
                storage_path=storage_path,
                access_url=access_url,
                uploaded_by=request.user,
                description=request.data.get('description', '')
            )
            
            serializer = MediaFileSerializer(media_file)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({'detail': f'文件上传失败: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def copy_url(self, request, pk=None):
        """复制文件访问URL"""
        media_file = self.get_object()
        return Response({
            'url': media_file.access_url,
            'html_code': f'<img src="{media_file.access_url}" alt="{media_file.file_name}" />',
            'markdown_code': f'![{media_file.file_name}]({media_file.access_url})',
        })
    
    @action(detail=True, methods=['delete'])
    def delete_file(self, request, pk=None):
        """删除媒体文件（同时删除存储中的文件）"""
        media_file = self.get_object()
        config = media_file.storage_config
        
        try:
            # 获取存储后端
            backend = get_storage_backend(config)
            
            # 删除存储中的文件
            backend.delete_file(media_file.storage_path)
            
            # 删除数据库记录
            media_file.delete()
            
            return Response({'detail': '文件已删除'}, status=status.HTTP_204_NO_CONTENT)
        
        except Exception as e:
            return Response({'detail': f'文件删除失败: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
    
    def _get_file_type(self, content_type, filename):
        """根据MIME类型和文件名获取文件类型"""
        if content_type.startswith('image/'):
            return 'image'
        elif content_type.startswith('video/'):
            return 'video'
        elif content_type.startswith('audio/'):
            return 'audio'
        elif content_type.startswith('application/') or filename.endswith(('.pdf', '.doc', '.docx', '.xls', '.xlsx', '.txt')):
            return 'document'
        return 'other'
