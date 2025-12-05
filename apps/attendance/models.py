from django.db import models
from apps.students.models import Student
from apps.classes.models import ClassSchedule


class Attendance(models.Model):
    """考勤记录"""
    
    STATUS_CHOICES = (
        ('present', '出勤'),
        ('absent', '缺勤'),
        ('leave', '请假'),
        ('late', '迟到'),
    )
    
    schedule = models.ForeignKey(ClassSchedule, on_delete=models.CASCADE, 
                                related_name='attendances', verbose_name='排课')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='学员')
    status = models.CharField('考勤状态', max_length=20, choices=STATUS_CHOICES)
    check_in_time = models.DateTimeField('签到时间', null=True, blank=True)
    notes = models.TextField('备注', null=True, blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        verbose_name = '考勤记录'
        verbose_name_plural = verbose_name
        db_table = 'attendances'
        ordering = ['-created_at']
        unique_together = ['schedule', 'student']
        app_label = 'attendance'
    
    def __str__(self):
        return f"{self.student.real_name} - {self.schedule} - {self.get_status_display()}"
