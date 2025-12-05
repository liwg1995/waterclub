import xadmin
from .models import Banner, Article, Gallery, Contact


class BannerAdmin:
    """轮播图管理"""
    list_display = ['title', 'sort_order', 'is_active', 'created_at']
    list_editable = ['sort_order', 'is_active']
    search_fields = ['title']


class ArticleAdmin:
    """文章管理"""
    list_display = ['title', 'category', 'author', 'views', 'is_published', 
                   'is_featured', 'published_at']
    list_filter = ['category', 'is_published', 'is_featured', 'published_at']
    search_fields = ['title', 'content']
    list_editable = ['is_published', 'is_featured']
    style_fields = {'content': 'ueditor'}


class GalleryAdmin:
    """作品相册管理"""
    list_display = ['title', 'sort_order', 'is_active', 'created_at']
    list_editable = ['sort_order', 'is_active']
    search_fields = ['title']


class ContactAdmin:
    """联系留言管理"""
    list_display = ['name', 'phone', 'subject', 'is_replied', 'created_at']
    list_filter = ['is_replied', 'created_at']
    search_fields = ['name', 'phone', 'subject']
    list_editable = ['is_replied']
    readonly_fields = ['name', 'phone', 'email', 'subject', 'message', 'created_at']


xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(Article, ArticleAdmin)
xadmin.site.register(Gallery, GalleryAdmin)
xadmin.site.register(Contact, ContactAdmin)
