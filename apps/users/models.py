from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """自定义用户模型"""
    
    USER_TYPE_CHOICES = (
        ('admin', '管理员'),
        ('staff', '教务人员'),
        ('teacher', '教师'),
        ('student', '学员'),
    )
    
    user_type = models.CharField('用户类型', max_length=20, choices=USER_TYPE_CHOICES, default='student')
    phone = models.CharField('手机号', max_length=11, unique=True, null=True, blank=True)
    avatar = models.ImageField('头像', upload_to='avatars/', null=True, blank=True)
    gender = models.CharField('性别', max_length=10, choices=(('male', '男'), ('female', '女'), ('other', '其他')), 
                             null=True, blank=True)
    birth_date = models.DateField('出生日期', null=True, blank=True)
    id_card = models.CharField('身份证号', max_length=18, null=True, blank=True)
    address = models.CharField('地址', max_length=200, null=True, blank=True)
    emergency_contact = models.CharField('紧急联系人', max_length=50, null=True, blank=True)
    emergency_phone = models.CharField('紧急联系电话', max_length=11, null=True, blank=True)
    notes = models.TextField('备注', null=True, blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        db_table = 'users'
        app_label = 'users'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"


class UserProfile(models.Model):
    """用户扩展信息"""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    wechat_openid = models.CharField('微信OpenID', max_length=100, null=True, blank=True, unique=True)
    wechat_unionid = models.CharField('微信UnionID', max_length=100, null=True, blank=True)
    alipay_user_id = models.CharField('支付宝用户ID', max_length=100, null=True, blank=True)
    points = models.IntegerField('积分', default=0)
    level = models.CharField('会员等级', max_length=20, default='普通会员')
    referrer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                                related_name='referrals', verbose_name='推荐人')
    
    class Meta:
        verbose_name = '用户扩展信息'
        verbose_name_plural = verbose_name
        db_table = 'user_profiles'
        app_label = 'users'
    
    def __str__(self):
        return f"{self.user.username} 的扩展信息"
