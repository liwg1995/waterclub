from django.db import models
from apps.teachers.models import Teacher
from apps.students.models import Student


class DanceType(models.Model):
    """舞种分类"""
    name = models.CharField('舞种名称', max_length=50, unique=True)
    description = models.TextField('描述', null=True, blank=True)
    icon = models.ImageField('图标', upload_to='dance_types/', null=True, blank=True)
    is_active = models.BooleanField('是否启用', default=True)
    
    class Meta:
        verbose_name = '舞种分类'
        verbose_name_plural = verbose_name
        db_table = 'dance_types'
        app_label = 'classes'
    
    def __str__(self):
        return self.name


class ClassType(models.Model):
    """班型（课程类型）"""
    
    LEVEL_CHOICES = (
        ('beginner', '初级'),
        ('intermediate', '中级'),
        ('advanced', '高级'),
        ('professional', '专业'),
    )
    
    name = models.CharField('班型名称', max_length=100)
    dance_type = models.ForeignKey(DanceType, on_delete=models.PROTECT, verbose_name='舞种')
    level = models.CharField('级别', max_length=20, choices=LEVEL_CHOICES)
    age_range = models.CharField('适龄范围', max_length=50, help_text='如：4-6岁')
    duration_minutes = models.IntegerField('单次课时长（分钟）', default=60)
    max_students = models.IntegerField('最大人数', default=20)
    description = models.TextField('课程简介', null=True, blank=True)
    syllabus = models.TextField('教学大纲', null=True, blank=True)
    cover_image = models.ImageField('封面图', upload_to='class_types/', null=True, blank=True)
    is_active = models.BooleanField('是否启用', default=True)
    sort_order = models.IntegerField('排序', default=0)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    
    class Meta:
        verbose_name = '班型'
        verbose_name_plural = verbose_name
        db_table = 'class_types'
        ordering = ['sort_order', '-created_at']
        app_label = 'classes'
    
    def __str__(self):
        return f"{self.name} ({self.get_level_display()})"


class Course(models.Model):
    """课程（开班实例）"""
    
    STATUS_CHOICES = (
        ('draft', '草稿'),
        ('enrolling', '招生中'),
        ('ongoing', '进行中'),
        ('completed', '已结束'),
        ('cancelled', '已取消'),
    )
    
    class_type = models.ForeignKey(ClassType, on_delete=models.PROTECT, verbose_name='班型')
    name = models.CharField('课程名称', max_length=100)
    term = models.CharField('期次', max_length=50, help_text='如：第1期')
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, verbose_name='授课教师')
    status = models.CharField('状态', max_length=20, choices=STATUS_CHOICES, default='draft')
    start_date = models.DateField('开课日期')
    end_date = models.DateField('结课日期')
    total_sessions = models.IntegerField('总课次', default=12)
    enrolled_count = models.IntegerField('已报名人数', default=0)
    max_students = models.IntegerField('招生名额', default=20)
    is_open_enrollment = models.BooleanField('是否开放报名', default=True)
    notes = models.TextField('备注', null=True, blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        verbose_name = '课程'
        verbose_name_plural = verbose_name
        db_table = 'courses'
        ordering = ['-created_at']
        app_label = 'classes'
    
    def __str__(self):
        return f"{self.name} - {self.term}"
    
    @property
    def is_full(self):
        """是否已满员"""
        return self.enrolled_count >= self.max_students


class ClassRoom(models.Model):
    """教室"""
    name = models.CharField('教室名称', max_length=50)
    capacity = models.IntegerField('容纳人数')
    location = models.CharField('位置', max_length=100)
    equipment = models.TextField('设备', null=True, blank=True)
    is_active = models.BooleanField('是否可用', default=True)
    
    class Meta:
        verbose_name = '教室'
        verbose_name_plural = verbose_name
        db_table = 'classrooms'
        app_label = 'classes'
    
    def __str__(self):
        return self.name


class ClassSchedule(models.Model):
    """排课"""
    
    STATUS_CHOICES = (
        ('scheduled', '正常'),
        ('rescheduled', '已调课'),
        ('cancelled', '已取消'),
    )
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='schedules', 
                              verbose_name='课程')
    session_no = models.IntegerField('第几课次')
    classroom = models.ForeignKey(ClassRoom, on_delete=models.PROTECT, verbose_name='教室')
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT, verbose_name='授课教师')
    start_time = models.DateTimeField('开始时间')
    end_time = models.DateTimeField('结束时间')
    status = models.CharField('状态', max_length=20, choices=STATUS_CHOICES, default='scheduled')
    actual_students = models.IntegerField('实际出勤', default=0)
    notes = models.TextField('备注', null=True, blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    
    class Meta:
        verbose_name = '排课'
        verbose_name_plural = verbose_name
        db_table = 'class_schedules'
        ordering = ['start_time']
        app_label = 'classes'
    
    def __str__(self):
        return f"{self.course.name} 第{self.session_no}课次"


class Enrollment(models.Model):
    """报名记录"""
    
    STATUS_CHOICES = (
        ('pending', '待支付'),
        ('paid', '已支付'),
        ('refunding', '退款中'),
        ('refunded', '已退款'),
        ('cancelled', '已取消'),
    )
    
    student = models.ForeignKey(Student, on_delete=models.PROTECT, verbose_name='学员')
    course = models.ForeignKey(Course, on_delete=models.PROTECT, verbose_name='课程')
    enrollment_date = models.DateTimeField('报名时间', auto_now_add=True)
    status = models.CharField('状态', max_length=20, choices=STATUS_CHOICES, default='pending')
    source = models.CharField('报名渠道', max_length=50, default='线上', 
                             help_text='线上/线下/电话等')
    price_policy = models.ForeignKey('finance.PricePolicy', on_delete=models.SET_NULL, 
                                    null=True, blank=True, verbose_name='价格策略')
    amount = models.DecimalField('应付金额', max_digits=10, decimal_places=2, default=0)
    payment_record = models.ForeignKey('payment.PaymentRecord', on_delete=models.SET_NULL,
                                      null=True, blank=True, verbose_name='支付记录')
    notes = models.TextField('备注', null=True, blank=True)
    
    class Meta:
        verbose_name = '报名记录'
        verbose_name_plural = verbose_name
        db_table = 'enrollments'
        ordering = ['-enrollment_date']
        unique_together = ['student', 'course']
        app_label = 'classes'
        indexes = [
            models.Index(fields=['student', 'status']),
            models.Index(fields=['course', 'status']),
        ]
    
    def __str__(self):
        return f"{self.student.real_name} 报名 {self.course.name}"
    
    def get_pay_url(self):
        """获取支付链接"""
        if self.status == 'paid':
            return None
        return f"/api/payment/create/?enrollment_id={self.pk}"
