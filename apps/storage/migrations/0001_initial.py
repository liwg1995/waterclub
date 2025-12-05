from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='StorageConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='配置名称')),
                ('storage_type', models.CharField(choices=[('local', '本地存储'), ('tencent_cos', '腾讯云对象存储（COS）'), ('aliyun_oss', '阿里云对象存储（OSS）'), ('qiniu', '七牛云存储'), ('minio', 'MinIO 对象存储')], max_length=20, verbose_name='存储类型')),
                ('is_active', models.BooleanField(default=False, help_text='同一时间只能启用一个存储配置', verbose_name='是否启用')),
                ('bucket_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='存储桶名称')),
                ('access_url', models.CharField(blank=True, help_text='例如：https://bucket.oss-cn-beijing.aliyuncs.com', max_length=500, null=True, verbose_name='访问URL前缀')),
                ('credentials', models.JSONField(blank=True, default=dict, help_text='根据存储类型存储相应的凭证信息', verbose_name='凭证信息')),
                ('max_file_size', models.IntegerField(default=100, help_text='单个文件最大大小，单位为MB', verbose_name='最大文件大小(MB)')),
                ('allowed_extensions', models.CharField(default='jpg,jpeg,png,gif,bmp,pdf,doc,docx,xls,xlsx,txt,mp4,avi', help_text='用逗号分隔，不包含点', max_length=255, verbose_name='允许的文件扩展名')),
                ('auto_create_dir', models.BooleanField(default=True, verbose_name='自动创建目录')),
                ('use_date_path', models.BooleanField(default=True, help_text='如启用，文件将保存在YYYY/MM/DD目录下', verbose_name='使用日期路径')),
                ('description', models.TextField(blank=True, null=True, verbose_name='配置说明')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '媒体存储配置',
                'verbose_name_plural': '媒体存储配置',
                'ordering': ['-is_active', '-created_at'],
            },
        ),
        migrations.CreateModel(
            name='MediaFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(max_length=255, verbose_name='原始文件名')),
                ('file_type', models.CharField(choices=[('image', '图片'), ('video', '视频'), ('audio', '音频'), ('document', '文档'), ('other', '其他')], max_length=20, verbose_name='文件类型')),
                ('file_size', models.BigIntegerField(verbose_name='文件大小(字节)')),
                ('storage_path', models.CharField(max_length=500, verbose_name='存储路径')),
                ('access_url', models.CharField(max_length=1000, verbose_name='访问URL')),
                ('description', models.TextField(blank=True, null=True, verbose_name='文件描述')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True, verbose_name='上传时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('storage_config', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='media_files', to='storage.storageconfig', verbose_name='存储配置')),
                ('uploaded_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='uploaded_files', to=settings.AUTH_USER_MODEL, verbose_name='上传者')),
            ],
            options={
                'verbose_name': '媒体文件',
                'verbose_name_plural': '媒体文件',
                'ordering': ['-uploaded_at'],
            },
        ),
        migrations.AddIndex(
            model_name='mediafile',
            index=models.Index(fields=['file_type', '-uploaded_at'], name='storage_med_file_ty_123456_idx'),
        ),
        migrations.AddIndex(
            model_name='mediafile',
            index=models.Index(fields=['storage_config', '-uploaded_at'], name='storage_med_storage_654321_idx'),
        ),
    ]
