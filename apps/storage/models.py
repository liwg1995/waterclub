from django.db import models
from django.core.validators import URLValidator
import json


class StorageConfig(models.Model):
    """媒体文件存储配置"""
    
    STORAGE_TYPE_CHOICES = [
        ('local', '本地存储'),
        ('tencent_cos', '腾讯云对象存储（COS）'),
        ('aliyun_oss', '阿里云对象存储（OSS）'),
        ('qiniu', '七牛云存储'),
        ('minio', 'MinIO 对象存储'),
    ]
    
    name = models.CharField('配置名称', max_length=100, unique=True)
    storage_type = models.CharField('存储类型', max_length=20, choices=STORAGE_TYPE_CHOICES)
    is_active = models.BooleanField('是否启用', default=False, help_text='同一时间只能启用一个存储配置')
    
    # 通用配置
    bucket_name = models.CharField('存储桶名称', max_length=255, blank=True, null=True)
    access_url = models.CharField('访问URL前缀', max_length=500, blank=True, null=True, 
                                 help_text='例如：https://bucket.oss-cn-beijing.aliyuncs.com')
    
    # 认证信息（JSON格式）
    credentials = models.JSONField('凭证信息', default=dict, blank=True,
                                  help_text='根据存储类型存储相应的凭证信息')
    
    # 高级选项
    max_file_size = models.IntegerField('最大文件大小(MB)', default=100,
                                       help_text='单个文件最大大小，单位为MB')
    allowed_extensions = models.CharField('允许的文件扩展名', max_length=255, 
                                         default='jpg,jpeg,png,gif,bmp,pdf,doc,docx,xls,xlsx,txt,mp4,avi',
                                         help_text='用逗号分隔，不包含点')
    auto_create_dir = models.BooleanField('自动创建目录', default=True)
    use_date_path = models.BooleanField('使用日期路径', default=True, 
                                       help_text='如启用，文件将保存在YYYY/MM/DD目录下')
    
    # 描述
    description = models.TextField('配置说明', blank=True, null=True)
    
    # 时间戳
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        verbose_name = '媒体存储配置'
        verbose_name_plural = '媒体存储配置'
        ordering = ['-is_active', '-created_at']
    
    def __str__(self):
        return f'{self.get_storage_type_display()} - {self.name}'
    
    def save(self, *args, **kwargs):
        """保存时确保只有一个存储配置被激活"""
        if self.is_active:
            # 将其他配置设为不激活
            StorageConfig.objects.exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)
    
    def get_credentials(self):
        """获取解析后的凭证信息"""
        return self.credentials if isinstance(self.credentials, dict) else json.loads(self.credentials or '{}')


class MediaFile(models.Model):
    """媒体文件记录"""
    
    FILE_TYPE_CHOICES = [
        ('image', '图片'),
        ('video', '视频'),
        ('audio', '音频'),
        ('document', '文档'),
        ('other', '其他'),
    ]
    
    # 文件信息
    file_name = models.CharField('原始文件名', max_length=255)
    file_type = models.CharField('文件类型', max_length=20, choices=FILE_TYPE_CHOICES)
    file_size = models.BigIntegerField('文件大小(字节)')
    
    # 存储信息
    storage_config = models.ForeignKey(StorageConfig, on_delete=models.PROTECT,
                                      verbose_name='存储配置', related_name='media_files')
    storage_path = models.CharField('存储路径', max_length=500)
    access_url = models.CharField('访问URL', max_length=1000)
    
    # 额外信息
    uploaded_by = models.ForeignKey('users.User', on_delete=models.SET_NULL,
                                   null=True, blank=True, verbose_name='上传者', related_name='uploaded_files')
    description = models.TextField('文件描述', blank=True, null=True)
    
    # 时间戳
    uploaded_at = models.DateTimeField('上传时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        verbose_name = '媒体文件'
        verbose_name_plural = '媒体文件'
        ordering = ['-uploaded_at']
        indexes = [
            models.Index(fields=['file_type', '-uploaded_at']),
            models.Index(fields=['storage_config', '-uploaded_at']),
        ]
    
    def __str__(self):
        return self.file_name
    
    @property
    def file_size_mb(self):
        """文件大小（MB）"""
        return round(self.file_size / (1024 * 1024), 2)
