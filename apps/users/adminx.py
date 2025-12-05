import xadmin
from xadmin import views
from .models import User, UserProfile


class BaseSetting:
    """xadmin基础配置"""
    enable_themes = True
    use_bootswatch = True


class GlobalSettings:
    """xadmin全局配置"""
    site_title = "水立方舞蹈工作室管理系统"
    site_footer = "Water Cube Dance Studio"
    menu_style = "accordion"


class UserAdmin:
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


class UserProfileAdmin:
    """用户扩展信息管理"""
    list_display = ['user', 'points', 'level', 'referrer']
    search_fields = ['user__username', 'wechat_openid']
    list_filter = ['level']


xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
xadmin.site.register(User, UserAdmin)
xadmin.site.register(UserProfile, UserProfileAdmin)
