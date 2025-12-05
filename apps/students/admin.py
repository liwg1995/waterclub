from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """学员管理"""
    list_display = ['student_no', 'real_name', 'status', 'remaining_classes', 
                   'enrollment_date', 'user']
    list_filter = ['status', 'enrollment_date']
    search_fields = ['student_no', 'real_name', 'user__phone', 'user__email']
    list_editable = ['status']
    readonly_fields = ['created_at', 'updated_at', 'total_spent']
    
    fieldsets = (
        ('基本信息', {
            'fields': ('user', 'student_no', 'real_name', 'nickname', 'status')
        }),
        ('监护人信息', {
            'fields': ('guardian_name', 'guardian_phone', 'guardian_relation')
        }),
        ('学习信息', {
            'fields': ('enrollment_date', 'graduation_date', 'total_classes', 
                      'remaining_classes', 'total_spent')
        }),
        ('健康与备注', {
            'fields': ('health_info', 'special_notes')
        }),
    )
