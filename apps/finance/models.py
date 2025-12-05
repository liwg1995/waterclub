from django.db import models
from apps.students.models import Student
from apps.classes.models import Course, Enrollment


class PricePolicy(models.Model):
    """价格策略"""
    
    BILLING_TYPE_CHOICES = (
        ('session_card', '次卡'),
        ('monthly', '月卡'),
        ('semester', '学期制'),
        ('hourly', '按课时'),
    )
    
    name = models.CharField('策略名称', max_length=100)
    billing_type = models.CharField('计费模式', max_length=20, choices=BILLING_TYPE_CHOICES)
    sessions = models.IntegerField('课次数量', null=True, blank=True, help_text='次卡模式')
    price = models.DecimalField('价格', max_digits=10, decimal_places=2)
    unit_price = models.DecimalField('单价', max_digits=10, decimal_places=2, help_text='单课时价格')
    discount = models.DecimalField('折扣', max_digits=3, decimal_places=2, default=1.00, 
                                  help_text='1.00表示无折扣，0.8表示8折')
    validity_days = models.IntegerField('有效期（天）', null=True, blank=True)
    description = models.TextField('说明', null=True, blank=True)
    is_active = models.BooleanField('是否启用', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    
    class Meta:
        verbose_name = '价格策略'
        verbose_name_plural = verbose_name
        db_table = 'price_policies'
        app_label = 'finance'
    
    def __str__(self):
        return self.name


class Payment(models.Model):
    """支付记录"""
    
    PAYMENT_METHOD_CHOICES = (
        ('wechat', '微信支付'),
        ('alipay', '支付宝'),
        ('cash', '现金'),
        ('bank_transfer', '银行转账'),
    )
    
    STATUS_CHOICES = (
        ('pending', '待支付'),
        ('paid', '已支付'),
        ('refunding', '退款中'),
        ('refunded', '已退款'),
        ('failed', '支付失败'),
    )
    
    order_no = models.CharField('订单号', max_length=50, unique=True)
    student = models.ForeignKey(Student, on_delete=models.PROTECT, verbose_name='学员')
    enrollment = models.ForeignKey(Enrollment, on_delete=models.SET_NULL, null=True, blank=True,
                                  verbose_name='关联报名')
    price_policy = models.ForeignKey(PricePolicy, on_delete=models.SET_NULL, null=True, 
                                    verbose_name='价格策略')
    amount = models.DecimalField('应付金额', max_digits=10, decimal_places=2)
    actual_amount = models.DecimalField('实付金额', max_digits=10, decimal_places=2)
    payment_method = models.CharField('支付方式', max_length=20, choices=PAYMENT_METHOD_CHOICES)
    status = models.CharField('状态', max_length=20, choices=STATUS_CHOICES, default='pending')
    transaction_id = models.CharField('交易号', max_length=100, null=True, blank=True)
    paid_at = models.DateTimeField('支付时间', null=True, blank=True)
    refunded_at = models.DateTimeField('退款时间', null=True, blank=True)
    refund_amount = models.DecimalField('退款金额', max_digits=10, decimal_places=2, default=0)
    notes = models.TextField('备注', null=True, blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    
    class Meta:
        verbose_name = '支付记录'
        verbose_name_plural = verbose_name
        db_table = 'payments'
        ordering = ['-created_at']
        app_label = 'finance'
    
    def __str__(self):
        return f"{self.order_no} - {self.student.real_name}"
