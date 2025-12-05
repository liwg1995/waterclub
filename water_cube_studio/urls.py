"""
URL configuration for water_cube_studio project.
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

# 配置Admin站点信息
admin.site.site_header = '水立方舞蹈工作室管理系统'
admin.site.site_title = '水立方舞蹈后台'
admin.site.index_title = '欢迎进入管理后台'

urlpatterns = [
    # Django admin后台
    path('admin/', admin.site.urls),
    
    # API文档
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    # API路由
    path('api/auth/', include('users.urls')),
    path('api/students/', include('students.urls')),
    path('api/teachers/', include('teachers.urls')),
    path('api/classes/', include('classes.urls')),
    path('api/finance/', include('finance.urls')),
    path('api/attendance/', include('attendance.urls')),
    path('api/payment/', include('apps.payment.urls')),  # 支付API
    path('api/storage/', include('apps.storage.urls')),  # 媒体存储API
    
    # 前端页面路由
    path('', include('cms.urls')),
    
    # CKEditor - 暂时注释
    # path('ckeditor/', include('ckeditor_uploader.urls')),
]

# 开发环境静态文件和媒体文件服务
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
