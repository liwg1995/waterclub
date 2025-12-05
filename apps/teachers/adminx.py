import xadmin
from .models import Teacher


class TeacherAdmin:
    """教师管理"""
    list_display = ['teacher_no', 'real_name', 'specialty', 'experience_years', 
                   'hourly_rate', 'status', 'join_date']
    list_filter = ['status', 'specialty', 'join_date']
    search_fields = ['teacher_no', 'real_name', 'user__phone']
    list_editable = ['status']
    
    fieldsets = (
        ('基本信息', {
            'fields': ('user', 'teacher_no', 'real_name', 'status', 'photo')
        }),
        ('教学信息', {
            'fields': ('specialty', 'experience_years', 'hourly_rate', 'introduction', 'achievements')
        }),
        ('任职信息', {
            'fields': ('join_date', 'leave_date')
        }),
    )


xadmin.site.register(Teacher, TeacherAdmin)
