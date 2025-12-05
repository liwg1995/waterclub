from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PricePolicyViewSet, PaymentViewSet

router = DefaultRouter()
router.register(r'price-policies', PricePolicyViewSet, basename='pricepolicy')
router.register(r'payments', PaymentViewSet, basename='payment')

urlpatterns = [
    path('', include(router.urls)),
]
