from django.contrib import admin
from .models import DanceType, ClassType, Course, ClassRoom, ClassSchedule, Enrollment


@admin.register(DanceType)
class DanceTypeAdmin(admin.ModelAdmin):
    """舞种管理"""
    list_display = ['name', 'is_active']
    list_editable = ['is_active']
    search_fields = ['name']


@admin.register(ClassType)
class ClassTypeAdmin(admin.ModelAdmin):
    """班型管理"""
    list_display = ['name', 'dance_type', 'level', 'age_range', 'duration_minutes', 
                   'max_students', 'is_active', 'sort_order']
    list_filter = ['dance_type', 'level', 'is_active']
    search_fields = ['name']
    list_editable = ['is_active', 'sort_order']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """课程管理"""
    list_display = ['name', 'class_type', 'term', 'teacher', 'status', 'start_date', 
                   'enrolled_count', 'max_students', 'is_open_enrollment']
    list_filter = ['status', 'class_type', 'start_date']
    search_fields = ['name', 'term']
    list_editable = ['status', 'is_open_enrollment']
    readonly_fields = ['enrolled_count']


@admin.register(ClassRoom)
class ClassRoomAdmin(admin.ModelAdmin):
    """教室管理"""
    list_display = ['name', 'capacity', 'location', 'is_active']
    list_editable = ['is_active']
    search_fields = ['name', 'location']


@admin.register(ClassSchedule)
class ClassScheduleAdmin(admin.ModelAdmin):
    """排课管理"""
    list_display = ['course', 'session_no', 'classroom', 'teacher', 'start_time', 
                   'status', 'actual_students']
    list_filter = ['status', 'start_time', 'classroom']
    search_fields = ['course__name', 'teacher__real_name']
    list_editable = ['status']


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    """报名管理"""
    list_display = ['student', 'course', 'enrollment_date', 'status', 'source']
    list_filter = ['status', 'source', 'enrollment_date']
    search_fields = ['student__real_name', 'course__name']
    list_editable = ['status']
