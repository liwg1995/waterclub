"""
Django settings for water_cube_studio project.
"""

import os
import sys
from pathlib import Path
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# 将apps目录添加到Python路径
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-default-key-change-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='*').split(',')

# Application definition
INSTALLED_APPS = [
    'simpleui',  # SimpleUI - Django Admin美化
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party apps
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    # 'django_redis',  # 暂时不使用Redis
    'ckeditor',
    # 'ckeditor_upload',  # 暂时注释，需要额外配置
    'import_export',
    'drf_spectacular',
    'crispy_forms',
    # 'crispy_bootstrap4',  # 暂时注释
    'reversion',
    
    # Custom apps
    'users.apps.UsersConfig',
    'students.apps.StudentsConfig',
    'teachers.apps.TeachersConfig',
    'classes.apps.ClassesConfig',
    'finance.apps.FinanceConfig',
    'cms.apps.CmsConfig',
    'attendance.apps.AttendanceConfig',
    'apps.payment.apps.PaymentConfig',  # 支付管理
    'apps.storage.apps.StorageConfig',  # 媒体存储配置
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # 静态文件服务
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'water_cube_studio.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
            ],
        },
    },
]

WSGI_APPLICATION = 'water_cube_studio.wsgi.application'

# Database - MySQL 8.0
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME', default='water_cube_db'),
        'USER': config('DB_USER', default='root'),
        'PASSWORD': config('DB_PASSWORD', default=''),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='3306'),
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom User Model
AUTH_USER_MODEL = 'users.User'

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# JWT Settings
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=2),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
}

# CORS Settings
CORS_ALLOW_ALL_ORIGINS = DEBUG
CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS', default='').split(',') if not DEBUG else []

# Redis Cache - 支持可选Redis配置
USE_REDIS = config('USE_REDIS', default=False, cast=bool)

if USE_REDIS:
    # 启用Redis缓存
    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': config('REDIS_URL', default='redis://127.0.0.1:6379/1'),
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
                'CONNECTION_POOL_KWARGS': {'max_connections': 50, 'retry_on_timeout': True},
                'SOCKET_CONNECT_TIMEOUT': 5,
                'SOCKET_TIMEOUT': 5,
            }
        }
    }
    # 使用Redis存储Session
    SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
    SESSION_CACHE_ALIAS = 'default'
    # 缓存超时时间（秒）
    CACHE_TIMEOUT = config('CACHE_TIMEOUT', default=3600, cast=int)
else:
    # 使用数据库缓存作为默认方案
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'unique-snowflake',
        }
    }
    # 使用数据库存储Session
    SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# CKEditor
CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 300,
        'width': '100%',
    },
}

# Crispy Forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"
CRISPY_TEMPLATE_PACK = "bootstrap4"

# Celery Configuration - 暂时不使用Celery
# CELERY_BROKER_URL = config('CELERY_BROKER_URL', default='redis://127.0.0.1:6379/0')
# CELERY_RESULT_BACKEND = config('CELERY_RESULT_BACKEND', default='redis://127.0.0.1:6379/0')
# CELERY_ACCEPT_CONTENT = ['json']
# CELERY_TASK_SERIALIZER = 'json']
# CELERY_RESULT_SERIALIZER = 'json']
# CELERY_TIMEZONE = TIME_ZONE

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# 创建logs目录
os.makedirs(BASE_DIR / 'logs', exist_ok=True)

# SimpleUI 配置
SIMPLEUI_DEFAULT_THEME = 'admin.lte.css'  # 默认主题
SIMPLEUI_HOME_INFO = False  # 隐藏首页快捷操作
SIMPLEUI_ANALYSIS = False  # 关闭分析
SIMPLEUI_CONFIG = {
    'system_keep': False,
    'menu_display': ['水立方舞蹈工作室', '用户管理', '学员管理', '教师管理', 
                     '班型课程', '财务管理', '支付配置', '考勤管理', '内容管理', '媒体管理'],
    'dynamic': True,
    'menus': [
        {
            'name': '首页',
            'icon': 'fa fa-home',
            'url': '/admin/'
        },
        {
            'app': 'users',
            'name': '用户管理',
            'icon': 'fa fa-users',
            'models': [
                {'name': '用户列表', 'icon': 'fa fa-user', 'url': '/admin/users/user/'},
                {'name': '用户资料', 'icon': 'fa fa-id-card', 'url': '/admin/users/userprofile/'},
            ]
        },
        {
            'app': 'students',
            'name': '学员管理',
            'icon': 'fa fa-graduation-cap',
            'models': [
                {'name': '学员列表', 'icon': 'fa fa-user-circle', 'url': '/admin/students/student/'},
            ]
        },
        {
            'app': 'teachers',
            'name': '教师管理',
            'icon': 'fa fa-chalkboard-teacher',
            'models': [
                {'name': '师资力量', 'icon': 'fa fa-user-tie', 'url': '/admin/teachers/teacher/'},
            ]
        },
        {
            'app': 'classes',
            'name': '班型课程',
            'icon': 'fa fa-book',
            'models': [
                {'name': '舞种管理', 'icon': 'fa fa-music', 'url': '/admin/classes/dancetype/'},
                {'name': '班型管理', 'icon': 'fa fa-layer-group', 'url': '/admin/classes/classtype/'},
                {'name': '课程管理', 'icon': 'fa fa-book-open', 'url': '/admin/classes/course/'},
                {'name': '教室管理', 'icon': 'fa fa-door-open', 'url': '/admin/classes/classroom/'},
                {'name': '排课管理', 'icon': 'fa fa-calendar-alt', 'url': '/admin/classes/classschedule/'},
                {'name': '报名管理', 'icon': 'fa fa-user-plus', 'url': '/admin/classes/enrollment/'},
            ]
        },
        {
            'app': 'finance',
            'name': '财务管理',
            'icon': 'fa fa-money-bill-wave',
            'models': [
                {'name': '价格策略', 'icon': 'fa fa-tag', 'url': '/admin/finance/pricepolicy/'},
                {'name': '支付记录', 'icon': 'fa fa-credit-card', 'url': '/admin/payment/paymentrecord/'},
            ]
        },
        {
            'app': 'payment',
            'name': '支付配置',
            'icon': 'fa fa-cog',
            'models': [
                {'name': '支付宝配置', 'icon': 'fa fa-alipay', 'url': '/admin/payment/alipayconfig/'},
                {'name': '微信支付配置', 'icon': 'fa fa-weixin', 'url': '/admin/payment/wechatpayconfig/'},
                {'name': '虎皮椒配置', 'icon': 'fa fa-leaf', 'url': '/admin/payment/hupipayconfig/'},
            ]
        },
        {
            'app': 'attendance',
            'name': '考勤管理',
            'icon': 'fa fa-clipboard-check',
            'models': [
                {'name': '考勤记录', 'icon': 'fa fa-check-circle', 'url': '/admin/attendance/attendance/'},
            ]
        },
        {
            'app': 'storage',
            'name': '媒体管理',
            'icon': 'fa fa-cloud-upload-alt',
            'models': [
                {'name': '存储配置', 'icon': 'fa fa-cog', 'url': '/admin/storage/storageconfig/'},
                {'name': '媒体文件', 'icon': 'fa fa-file-image', 'url': '/admin/storage/mediafile/'},
            ]
        },
        {
            'app': 'cms',
            'name': '内容管理',
            'icon': 'fa fa-newspaper',
            'models': [
                {'name': '轮播图', 'icon': 'fa fa-images', 'url': '/admin/cms/banner/'},
                {'name': '文章管理', 'icon': 'fa fa-file-alt', 'url': '/admin/cms/article/'},
                {'name': '作品展示', 'icon': 'fa fa-photo-video', 'url': '/admin/cms/gallery/'},
                {'name': '联系留言', 'icon': 'fa fa-envelope', 'url': '/admin/cms/contact/'},
            ]
        },
    ]
}
