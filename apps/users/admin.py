from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserProfile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """用户管理"""
    list_display = ['username', 'user_type', 'phone', 'email', 'is_active', 'date_joined']
    list_filter = ['user_type', 'is_active', 'date_joined']
    search_fields = ['username', 'phone', 'email', 'first_name', 'last_name']
    list_editable = ['is_active']
    readonly_fields = ['date_joined', 'last_login']
    fieldsets = (
        ('基本信息', {
            'fields': ('username', 'password', 'user_type')
        }),
        ('个人信息', {
            'fields': ('first_name', 'last_name', 'phone', 'email', 'gender', 'birth_date', 
                      'id_card', 'address', 'avatar')
        }),
        ('紧急联系', {
            'fields': ('emergency_contact', 'emergency_phone')
        }),
        ('权限', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('其他', {
            'fields': ('notes', 'date_joined', 'last_login')
        }),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """用户扩展信息管理"""
    list_display = ['user', 'points', 'level', 'referrer']
    search_fields = ['user__username', 'wechat_openid']
    list_filter = ['level']
