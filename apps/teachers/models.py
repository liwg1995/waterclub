from django.db import models
from apps.users.models import User


class Teacher(models.Model):
    """教师信息"""
    
    STATUS_CHOICES = (
        ('active', '在职'),
        ('leave', '请假'),
        ('resigned', '离职'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile', 
                               verbose_name='关联用户')
    teacher_no = models.CharField('教师编号', max_length=20, unique=True)
    real_name = models.CharField('真实姓名', max_length=50)
    specialty = models.CharField('擅长舞种', max_length=100)
    experience_years = models.IntegerField('教龄（年）', default=0)
    status = models.CharField('状态', max_length=20, choices=STATUS_CHOICES, default='active')
    introduction = models.TextField('个人简介', null=True, blank=True)
    achievements = models.TextField('教学成果', null=True, blank=True)
    hourly_rate = models.DecimalField('课时费（元/课时）', max_digits=8, decimal_places=2, default=0)
    photo = models.ImageField('照片', upload_to='teachers/', null=True, blank=True)
    join_date = models.DateField('入职日期')
    leave_date = models.DateField('离职日期', null=True, blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        verbose_name = '教师'
        verbose_name_plural = verbose_name
        db_table = 'teachers'
        ordering = ['-created_at']
        app_label = 'teachers'
    
    def __str__(self):
        return f"{self.real_name} ({self.teacher_no})"
