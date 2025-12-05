from django.contrib import admin
from .models import AlipayConfig, WeChatPayConfig, HuPiPayConfig

@admin.register(AlipayConfig)
class AlipayConfigAdmin(admin.ModelAdmin):
    """支付宝配置管理"""
    list_display = ['app_id', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['app_id']
    list_editable = ['is_active']
    
    fieldsets = (
        ('基本配置', {
            'fields': ('app_id', 'private_key', 'alipay_public_key')
        }),
        ('回调配置', {
            'fields': ('notify_url', 'return_url')
        }),
        ('状态', {
            'fields': ('is_active',)
        }),
    )


@admin.register(WeChatPayConfig)
class WeChatPayConfigAdmin(admin.ModelAdmin):
    """微信支付配置管理"""
    list_display = ['app_id', 'mch_id', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['app_id', 'mch_id']
    list_editable = ['is_active']
    
    fieldsets = (
        ('基本配置', {
            'fields': ('app_id', 'mch_id', 'api_key')
        }),
        ('证书配置', {
            'fields': ('cert_path', 'key_path')
        }),
        ('回调配置', {
            'fields': ('notify_url',)
        }),
        ('状态', {
            'fields': ('is_active',)
        }),
    )


@admin.register(HuPiPayConfig)
class HuPiPayConfigAdmin(admin.ModelAdmin):
    """虎皮椒支付配置管理"""
    list_display = ['app_id', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['app_id']
    list_editable = ['is_active']
    
    fieldsets = (
        ('基本配置', {
            'fields': ('app_id', 'app_secret')
        }),
        ('回调配置', {
            'fields': ('notify_url', 'return_url')
        }),
        ('状态', {
            'fields': ('is_active',)
        }),
    )
