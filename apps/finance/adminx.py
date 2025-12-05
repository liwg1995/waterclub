import xadmin
from .models import PricePolicy, Payment


class PricePolicyAdmin:
    """价格策略管理"""
    list_display = ['name', 'billing_type', 'price', 'unit_price', 'discount', 
                   'validity_days', 'is_active']
    list_filter = ['billing_type', 'is_active']
    search_fields = ['name']
    list_editable = ['is_active']


class PaymentAdmin:
    """支付记录管理"""
    list_display = ['order_no', 'student', 'amount', 'actual_amount', 'payment_method', 
                   'status', 'paid_at', 'created_at']
    list_filter = ['status', 'payment_method', 'created_at']
    search_fields = ['order_no', 'transaction_id', 'student__real_name']
    readonly_fields = ['order_no', 'transaction_id', 'paid_at', 'refunded_at']


xadmin.site.register(PricePolicy, PricePolicyAdmin)
xadmin.site.register(Payment, PaymentAdmin)
