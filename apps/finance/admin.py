from django.contrib import admin
from .models import PricePolicy, Payment
from apps.payment.models import PaymentRecord


@admin.register(PricePolicy)
class PricePolicyAdmin(admin.ModelAdmin):
    """价格策略管理"""
    list_display = ['name', 'billing_type', 'price', 'unit_price', 'discount', 
                   'validity_days', 'is_active']
    list_filter = ['billing_type', 'is_active']
    search_fields = ['name']
    list_editable = ['is_active']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """支付记录管理"""
    list_display = ['order_no', 'student', 'amount', 'actual_amount', 'payment_method', 
                   'status', 'paid_at', 'created_at']
    list_filter = ['status', 'payment_method', 'created_at']
    search_fields = ['order_no', 'transaction_id', 'student__real_name']
    readonly_fields = ['order_no', 'transaction_id', 'paid_at', 'refunded_at']


@admin.register(PaymentRecord)
class PaymentRecordAdmin(admin.ModelAdmin):
    """支付记录管理（payment应用）"""
    list_display = ['order_no', 'student', 'amount', 'payment_method', 'status', 
                   'transaction_id', 'paid_at', 'created_at']
    list_filter = ['payment_method', 'status', 'created_at']
    search_fields = ['order_no', 'transaction_id', 'student__real_name']
    list_editable = ['status']
    readonly_fields = ['order_no', 'transaction_id', 'paid_at', 'refunded_at', 'created_at', 'updated_at']
    
    fieldsets = (
        ('基本信息', {
            'fields': ('student', 'order_no', 'amount', 'payment_method', 'status')
        }),
        ('交易信息', {
            'fields': ('transaction_id', 'paid_at', 'refunded_at')
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
