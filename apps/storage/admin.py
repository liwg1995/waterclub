from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Count
from .models import StorageConfig, MediaFile


@admin.register(StorageConfig)
class StorageConfigAdmin(admin.ModelAdmin):
    """存储配置管理"""
    
    list_display = ['name', 'storage_type_display', 'active_status', 'bucket_name', 'access_url', 'media_count', 'updated_at']
    list_filter = ['storage_type', 'is_active', 'created_at']
    search_fields = ['name', 'bucket_name', 'access_url']
    readonly_fields = ['created_at', 'updated_at', 'media_count_display']
    
    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'storage_type', 'is_active', 'description')
        }),
        ('存储配置', {
            'fields': ('bucket_name', 'access_url')
        }),
        ('认证凭证', {
            'fields': ('credentials',),
            'description': '<strong>根据存储类型填写相应的凭证信息：</strong><br>'
                          '<strong>本地存储：</strong>无需填写<br>'
                          '<strong>腾讯COS：</strong>{"secret_id": "xxx", "secret_key": "xxx", "region": "xxx"}<br>'
                          '<strong>阿里OSS：</strong>{"access_key_id": "xxx", "access_key_secret": "xxx", "region": "xxx"}<br>'
                          '<strong>七牛云：</strong>{"access_key": "xxx", "secret_key": "xxx"}<br>'
                          '<strong>MinIO：</strong>{"access_key": "xxx", "secret_key": "xxx", "endpoint": "xxx"}'
        }),
        ('高级选项', {
            'fields': ('max_file_size', 'allowed_extensions', 'auto_create_dir', 'use_date_path'),
            'classes': ('collapse',)
        }),
        ('统计信息', {
            'fields': ('media_count_display', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def storage_type_display(self, obj):
        """存储类型显示"""
        colors = {
            'local': '#17a2b8',
            'tencent_cos': '#28a745',
            'aliyun_oss': '#dc3545',
            'qiniu': '#ffc107',
            'minio': '#6610f2',
        }
        color = colors.get(obj.storage_type, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color,
            obj.get_storage_type_display()
        )
    storage_type_display.short_description = '存储类型'
    
    def active_status(self, obj):
        """激活状态"""
        if obj.is_active:
            return format_html('<span style="color: green; font-weight: bold;">✓ 启用</span>')
        else:
            return format_html('<span style="color: gray;">○ 未启用</span>')
    active_status.short_description = '状态'
    
    def media_count(self, obj):
        """媒体文件数量"""
        count = obj.media_files.count()
        return format_html('<strong>{}</strong> 个文件', count)
    media_count.short_description = '文件数量'
    
    def media_count_display(self, obj):
        """媒体文件数量展示"""
        count = obj.media_files.count()
        return f'{count} 个文件'
    media_count_display.short_description = '媒体文件数量'
    
    actions = ['activate_storage']
    
    def activate_storage(self, request, queryset):
        """激活选中的存储配置"""
        if queryset.count() == 1:
            queryset.update(is_active=True)
            # 禁用其他配置
            StorageConfig.objects.exclude(pk=queryset.first().pk).update(is_active=False)
            self.message_user(request, '存储配置已激活')
        else:
            self.message_user(request, '请只选择一个存储配置', level=40)
    activate_storage.short_description = '激活选中的存储配置'


@admin.register(MediaFile)
class MediaFileAdmin(admin.ModelAdmin):
    """媒体文件管理"""
    
    list_display = ['file_name', 'file_type', 'file_size_mb', 'storage_config', 'access_link', 'uploaded_by', 'uploaded_at']
    list_filter = ['file_type', 'storage_config', 'uploaded_at']
    search_fields = ['file_name', 'storage_path', 'access_url']
    readonly_fields = ['uploaded_at', 'updated_at', 'file_size_mb', 'access_link', 'copy_link_html']
    date_hierarchy = 'uploaded_at'
    
    fieldsets = (
        ('文件信息', {
            'fields': ('file_name', 'file_type', 'file_size_mb', 'description')
        }),
        ('存储信息', {
            'fields': ('storage_config', 'storage_path', 'access_url', 'access_link')
        }),
        ('上传信息', {
            'fields': ('uploaded_by', 'uploaded_at', 'updated_at')
        }),
        ('复制链接', {
            'fields': ('copy_link_html',),
            'description': '点击下方按钮复制访问链接到剪贴板'
        }),
    )
    
    def access_link(self, obj):
        """访问链接"""
        if obj.access_url:
            return format_html(
                '<a href="{url}" target="_blank" style="color: #0066cc;">{url}</a>',
                url=obj.access_url
            )
        return '-'
    access_link.short_description = '访问链接'
    
    def copy_link_html(self, obj):
        """复制链接HTML"""
        if obj.access_url:
            return format_html(
                '''<div style="display: flex; gap: 10px;">
                    <input type="text" id="access_url" value="{url}" 
                           style="flex: 1; padding: 8px; border: 1px solid #ddd; border-radius: 4px;" readonly>
                    <button onclick="copyToClipboard()" style="padding: 8px 15px; background-color: #007bff; 
                                    color: white; border: none; border-radius: 4px; cursor: pointer;">复制</button>
                </div>
                <script>
                function copyToClipboard() {{
                    var url = document.getElementById('access_url');
                    url.select();
                    document.execCommand('copy');
                    alert('链接已复制到剪贴板！');
                }}
                </script>''',
                url=obj.access_url
            )
        return '暂无访问链接'
    copy_link_html.short_description = '快速复制'
    
    def file_size_mb(self, obj):
        """文件大小（MB）"""
        return f'{obj.file_size_mb} MB'
    file_size_mb.short_description = '文件大小'
    
    def has_add_permission(self, request):
        """禁止通过后台直接添加，应通过上传接口添加"""
        return False
    
    def has_delete_permission(self, request, obj=None):
        """允许删除"""
        return True
    
    actions = ['delete_selected_media']
    
    def delete_selected_media(self, request, queryset):
        """删除选中的媒体文件"""
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f'已删除 {count} 个媒体文件')
    delete_selected_media.short_description = '删除选中的媒体文件'
