from django.urls import path
from . import views

app_name = 'payment'
urlpatterns = [
    # 支付创建和管理
    path('create/', views.create_payment, name='create'),
    path('list/', views.payment_list, name='list'),
    path('success/', views.payment_success, name='success'),
    path('failure/', views.payment_failure, name='failure'),
    # 支付回调
    path('alipay/notify/', views.alipay_notify, name='alipay_notify'),
    path('alipay/return/', views.alipay_return, name='alipay_return'),
    path('wechat/notify/', views.wechat_notify, name='wechat_notify'),
    path('hupipay/notify/', views.hupipay_notify, name='hupipay_notify'),
]
