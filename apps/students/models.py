from django.db import models
from apps.users.models import User


class Student(models.Model):
    """学员信息"""
    
    STATUS_CHOICES = (
        ('active', '在读'),
        ('suspended', '休学'),
        ('graduated', '结业'),
        ('dropped', '退学'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile', 
                               verbose_name='关联用户')
    student_no = models.CharField('学号', max_length=20, unique=True)
    real_name = models.CharField('真实姓名', max_length=50)
    nickname = models.CharField('昵称', max_length=50, null=True, blank=True)
    status = models.CharField('学籍状态', max_length=20, choices=STATUS_CHOICES, default='active')
    enrollment_date = models.DateField('入学日期', auto_now_add=True)
    graduation_date = models.DateField('结业日期', null=True, blank=True)
    guardian_name = models.CharField('监护人姓名', max_length=50, null=True, blank=True)
    guardian_phone = models.CharField('监护人电话', max_length=11, null=True, blank=True)
    guardian_relation = models.CharField('监护人关系', max_length=20, null=True, blank=True)
    health_info = models.TextField('健康信息', null=True, blank=True, help_text='过敏史、既往病史等')
    special_notes = models.TextField('特殊说明', null=True, blank=True)
    total_classes = models.IntegerField('总课时', default=0)
    remaining_classes = models.IntegerField('剩余课时', default=0)
    total_spent = models.DecimalField('累计消费', max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        verbose_name = '学员'
        verbose_name_plural = verbose_name
        db_table = 'students'
        ordering = ['-created_at']
        app_label = 'students'
    
    def __str__(self):
        return f"{self.real_name} ({self.student_no})"
