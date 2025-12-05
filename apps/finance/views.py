from rest_framework import viewsets
from apps.finance.models import PricePolicy, Payment
from .serializers import PricePolicySerializer, PaymentSerializer


class PricePolicyViewSet(viewsets.ModelViewSet):
    """价格策略视图集"""
    queryset = PricePolicy.objects.filter(is_active=True)
    serializer_class = PricePolicySerializer


class PaymentViewSet(viewsets.ModelViewSet):
    """支付记录视图集"""
    queryset = Payment.objects.select_related('student', 'price_policy').all()
    serializer_class = PaymentSerializer
    filterset_fields = ['status', 'payment_method', 'student']
