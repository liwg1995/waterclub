from django.contrib import admin
from .models import Banner, Article, Gallery, Contact


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    """轮播图管理"""
    list_display = ['title', 'sort_order', 'is_active', 'created_at']
    list_editable = ['sort_order', 'is_active']
    search_fields = ['title']


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """文章管理"""
    list_display = ['title', 'category', 'author', 'views', 'is_published', 
                   'is_featured', 'published_at']
    list_filter = ['category', 'is_published', 'is_featured', 'published_at']
    search_fields = ['title', 'content']
    list_editable = ['is_published', 'is_featured']


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    """作品相册管理"""
    list_display = ['title', 'sort_order', 'is_active', 'created_at']
    list_editable = ['sort_order', 'is_active']
    search_fields = ['title']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """联系留言管理"""
    list_display = ['name', 'phone', 'subject', 'is_replied', 'created_at']
    list_filter = ['is_replied', 'created_at']
    search_fields = ['name', 'phone', 'subject']
    list_editable = ['is_replied']
    readonly_fields = ['name', 'phone', 'email', 'subject', 'message', 'created_at']
