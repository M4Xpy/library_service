from django.urls import path, include
from rest_framework import routers

router = routers.DefaultRouter()

from payments.views import PaymentViewSet

router.register(
    "",
    PaymentViewSet,
)

urlpatterns = [path("", include(router.urls))]

app_name = "payments"
