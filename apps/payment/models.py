from django.db import models
from django.conf import settings
from apps.students.models import Student


class PaymentRecord(models.Model):
    """支付记录"""
    PAYMENT_METHOD_CHOICES = [
        ('alipay_web', '支付宝网页支付'),
        ('alipay_qr', '支付宝当面付'),
        ('wechat_pay', '微信支付'),
        ('hupi_pay', '虎皮椒支付'),
    ]
    
    STATUS_CHOICES = [
        ('pending', '待支付'),
        ('paid', '已支付'),
        ('failed', '支付失败'),
        ('refunded', '已退款'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='学员')
    order_no = models.CharField('订单号', max_length=64, unique=True)
    amount = models.DecimalField('金额', max_digits=10, decimal_places=2)
    payment_method = models.CharField('支付方式', max_length=20, choices=PAYMENT_METHOD_CHOICES)
    status = models.CharField('状态', max_length=20, choices=STATUS_CHOICES, default='pending')
    transaction_id = models.CharField('交易号', max_length=128, blank=True, null=True)
    paid_at = models.DateTimeField('支付时间', blank=True, null=True)
    refunded_at = models.DateTimeField('退款时间', blank=True, null=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        verbose_name = '支付记录'
        verbose_name_plural = '支付记录'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.order_no} - {self.get_payment_method_display()} - {self.amount}'


class AlipayConfig(models.Model):
    """支付宝配置"""
    app_id = models.CharField('App ID', max_length=64)
    private_key = models.TextField('商户私钥')
    alipay_public_key = models.TextField('支付宝公钥')
    notify_url = models.URLField('异步通知地址', blank=True)
    return_url = models.URLField('同步跳转地址', blank=True)
    is_active = models.BooleanField('是否启用', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    
    class Meta:
        verbose_name = '支付宝配置'
        verbose_name_plural = '支付宝配置'
    
    def __str__(self):
        return f'支付宝配置 - {self.app_id}'


class WeChatPayConfig(models.Model):
    """微信支付配置"""
    app_id = models.CharField('App ID', max_length=64)
    mch_id = models.CharField('商户号', max_length=32)
    api_key = models.CharField('API密钥', max_length=64)
    cert_path = models.CharField('证书路径', max_length=255, blank=True)
    key_path = models.CharField('密钥路径', max_length=255, blank=True)
    notify_url = models.URLField('异步通知地址', blank=True)
    is_active = models.BooleanField('是否启用', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    
    class Meta:
        verbose_name = '微信支付配置'
        verbose_name_plural = '微信支付配置'
    
    def __str__(self):
        return f'微信支付配置 - {self.app_id}'


class HuPiPayConfig(models.Model):
    """虎皮椒支付配置"""
    app_id = models.CharField('App ID', max_length=64)
    app_secret = models.CharField('App Secret', max_length=128)
    notify_url = models.URLField('异步通知地址', blank=True)
    return_url = models.URLField('同步跳转地址', blank=True)
    is_active = models.BooleanField('是否启用', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    
    class Meta:
        verbose_name = '虎皮椒支付配置'
        verbose_name_plural = '虎皮椒支付配置'
    
    def __str__(self):
        return f'虎皮椒支付配置 - {self.app_id}'
