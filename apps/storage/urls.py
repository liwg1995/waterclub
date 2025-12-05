from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StorageConfigViewSet, MediaFileViewSet

router = DefaultRouter()
router.register(r'storage-configs', StorageConfigViewSet, basename='storage-config')
router.register(r'media-files', MediaFileViewSet, basename='media-file')

urlpatterns = [
    path('', include(router.urls)),
]
