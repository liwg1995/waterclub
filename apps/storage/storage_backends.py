"""
存储后端实现 - 支持多种存储方案
"""

import os
from datetime import datetime
from django.conf import settings
from django.core.files.storage import default_storage
from pathlib import Path


class BaseStorageBackend:
    """存储后端基类"""
    
    def __init__(self, config):
        self.config = config
    
    def validate_file(self, file_obj):
        """验证文件"""
        # 检查文件大小
        max_size_bytes = self.config.max_file_size * 1024 * 1024
        if file_obj.size > max_size_bytes:
            return f'文件大小不能超过 {self.config.max_file_size} MB'
        
        # 检查文件扩展名
        allowed_exts = [ext.strip().lower() for ext in self.config.allowed_extensions.split(',')]
        file_ext = os.path.splitext(file_obj.name)[1].lstrip('.').lower()
        if file_ext not in allowed_exts:
            return f'不支持的文件类型: {file_ext}。允许的类型: {", ".join(allowed_exts)}'
        
        return None
    
    def get_storage_path(self, filename):
        """生成存储路径"""
        if self.config.use_date_path:
            now = datetime.now()
            date_path = now.strftime('%Y/%m/%d')
            return f'uploads/{date_path}/{filename}'
        else:
            return f'uploads/{filename}'
    
    def upload_file(self, file_obj):
        """上传文件，返回 (storage_path, access_url)"""
        raise NotImplementedError
    
    def delete_file(self, storage_path):
        """删除文件"""
        raise NotImplementedError


class LocalStorageBackend(BaseStorageBackend):
    """本地存储后端"""
    
    def upload_file(self, file_obj):
        """上传到本地存储"""
        storage_path = self.get_storage_path(file_obj.name)
        
        # 确保目录存在
        media_root = settings.MEDIA_ROOT
        full_path = os.path.join(media_root, storage_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        # 保存文件
        with open(full_path, 'wb') as f:
            for chunk in file_obj.chunks():
                f.write(chunk)
        
        # 生成访问URL
        access_url = f'{settings.MEDIA_URL}{storage_path}'
        
        return storage_path, access_url


class TencentCOSBackend(BaseStorageBackend):
    """腾讯云对象存储（COS）后端"""
    
    def upload_file(self, file_obj):
        """上传到腾讯COS"""
        try:
            from cos import CosConfig, CosS3Client
        except ImportError:
            raise ImportError('请先安装cos-python-sdk: pip install cos-python-sdk-v5')
        
        credentials = self.config.get_credentials()
        secret_id = credentials.get('secret_id')
        secret_key = credentials.get('secret_key')
        region = credentials.get('region')
        
        if not all([secret_id, secret_key, region]):
            raise ValueError('腾讯COS凭证不完整')
        
        # 初始化COS客户端
        config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key)
        client = CosS3Client(config)
        
        storage_path = self.get_storage_path(file_obj.name)
        
        # 上传文件
        client.put_object(
            Bucket=self.config.bucket_name,
            Key=storage_path,
            Body=file_obj.read()
        )
        
        # 生成访问URL
        access_url = f'{self.config.access_url}/{storage_path}'
        
        return storage_path, access_url
    
    def delete_file(self, storage_path):
        """删除腾讯COS中的文件"""
        try:
            from cos import CosConfig, CosS3Client
        except ImportError:
            raise ImportError('请先安装cos-python-sdk: pip install cos-python-sdk-v5')
        
        credentials = self.config.get_credentials()
        config = CosConfig(
            Region=credentials.get('region'),
            SecretId=credentials.get('secret_id'),
            SecretKey=credentials.get('secret_key')
        )
        client = CosS3Client(config)
        client.delete_object(Bucket=self.config.bucket_name, Key=storage_path)


class AliyunOSSBackend(BaseStorageBackend):
    """阿里云对象存储（OSS）后端"""
    
    def upload_file(self, file_obj):
        """上传到阿里OSS"""
        try:
            import oss2
        except ImportError:
            raise ImportError('请先安装oss2: pip install oss2')
        
        credentials = self.config.get_credentials()
        access_key_id = credentials.get('access_key_id')
        access_key_secret = credentials.get('access_key_secret')
        region = credentials.get('region')
        
        if not all([access_key_id, access_key_secret, region]):
            raise ValueError('阿里OSS凭证不完整')
        
        # 初始化OSS客户端
        endpoint = f'https://oss-cn-{region}.aliyuncs.com' if 'http' not in region else region
        auth = oss2.Auth(access_key_id, access_key_secret)
        bucket = oss2.Bucket(auth, endpoint, self.config.bucket_name)
        
        storage_path = self.get_storage_path(file_obj.name)
        
        # 上传文件
        bucket.put_object(storage_path, file_obj.read())
        
        # 生成访问URL
        access_url = f'{self.config.access_url}/{storage_path}'
        
        return storage_path, access_url
    
    def delete_file(self, storage_path):
        """删除阿里OSS中的文件"""
        try:
            import oss2
        except ImportError:
            raise ImportError('请先安装oss2: pip install oss2')
        
        credentials = self.config.get_credentials()
        region = credentials.get('region')
        endpoint = f'https://oss-cn-{region}.aliyuncs.com' if 'http' not in region else region
        auth = oss2.Auth(credentials.get('access_key_id'), credentials.get('access_key_secret'))
        bucket = oss2.Bucket(auth, endpoint, self.config.bucket_name)
        bucket.delete_object(storage_path)


class QiniuBackend(BaseStorageBackend):
    """七牛云存储后端"""
    
    def upload_file(self, file_obj):
        """上传到七牛云"""
        try:
            from qiniu import Auth, put_data
        except ImportError:
            raise ImportError('请先安装qiniu: pip install qiniu')
        
        credentials = self.config.get_credentials()
        access_key = credentials.get('access_key')
        secret_key = credentials.get('secret_key')
        
        if not all([access_key, secret_key]):
            raise ValueError('七牛云凭证不完整')
        
        # 初始化七牛云认证
        q = Auth(access_key, secret_key)
        token = q.upload_token(self.config.bucket_name)
        
        storage_path = self.get_storage_path(file_obj.name)
        
        # 上传文件
        ret, info = put_data(token, storage_path, file_obj.read())
        
        if not ret:
            raise Exception(f'七牛云上传失败: {info}')
        
        # 生成访问URL
        access_url = f'{self.config.access_url}/{storage_path}'
        
        return storage_path, access_url
    
    def delete_file(self, storage_path):
        """删除七牛云中的文件"""
        try:
            from qiniu import Auth
        except ImportError:
            raise ImportError('请先安装qiniu: pip install qiniu')
        
        credentials = self.config.get_credentials()
        q = Auth(credentials.get('access_key'), credentials.get('secret_key'))
        q.delete(self.config.bucket_name, storage_path)


class MinIOBackend(BaseStorageBackend):
    """MinIO对象存储后端"""
    
    def upload_file(self, file_obj):
        """上传到MinIO"""
        try:
            from minio import Minio
        except ImportError:
            raise ImportError('请先安装minio: pip install minio')
        
        credentials = self.config.get_credentials()
        access_key = credentials.get('access_key')
        secret_key = credentials.get('secret_key')
        endpoint = credentials.get('endpoint')
        
        if not all([access_key, secret_key, endpoint]):
            raise ValueError('MinIO凭证不完整')
        
        # 初始化MinIO客户端
        client = Minio(endpoint, access_key=access_key, secret_key=secret_key)
        
        storage_path = self.get_storage_path(file_obj.name)
        
        # 上传文件
        client.put_object(
            self.config.bucket_name,
            storage_path,
            file_obj,
            length=file_obj.size
        )
        
        # 生成访问URL
        access_url = f'{self.config.access_url}/{storage_path}'
        
        return storage_path, access_url
    
    def delete_file(self, storage_path):
        """删除MinIO中的文件"""
        try:
            from minio import Minio
        except ImportError:
            raise ImportError('请先安装minio: pip install minio')
        
        credentials = self.config.get_credentials()
        client = Minio(
            credentials.get('endpoint'),
            access_key=credentials.get('access_key'),
            secret_key=credentials.get('secret_key')
        )
        client.remove_object(self.config.bucket_name, storage_path)


def get_storage_backend(config):
    """根据存储配置获取存储后端"""
    
    backends = {
        'local': LocalStorageBackend,
        'tencent_cos': TencentCOSBackend,
        'aliyun_oss': AliyunOSSBackend,
        'qiniu': QiniuBackend,
        'minio': MinIOBackend,
    }
    
    backend_class = backends.get(config.storage_type)
    if not backend_class:
        raise ValueError(f'未知的存储类型: {config.storage_type}')
    
    return backend_class(config)
