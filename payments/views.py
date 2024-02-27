from rest_framework import viewsets

from payments.models import Payment
from payments.serializers import PaymentSerializer
from users.permissions import IsAdminOrIfAuthenticatedReadOnly


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = IsAdminOrIfAuthenticatedReadOnly,
