from rest_framework import serializers
from apps.finance.models import PricePolicy, Payment


class PricePolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = PricePolicy
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.real_name', read_only=True)
    
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ['order_no', 'transaction_id', 'paid_at', 'refunded_at']
