import xadmin
from .models import Attendance


class AttendanceAdmin:
    """考勤管理"""
    list_display = ['schedule', 'student', 'status', 'check_in_time', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['student__real_name', 'schedule__course__name']
    list_editable = ['status']


xadmin.site.register(Attendance, AttendanceAdmin)
