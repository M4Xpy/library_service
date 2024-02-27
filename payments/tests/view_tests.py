from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from payments.models import Payment
from payments.serializers import PaymentSerializer
from payments.views import PaymentViewSet


class PaymentViewSetTestCase(TestCase):
    def setUp(self):
        self.payment1 = Payment.objects.create(
            status=Payment.StatusChoices.PENDING,
            payment_type=Payment.TypeChoices.PAYMENT,
            borrowing_id=1,
            session_url="http://example.com",
            session_id=123,
            money_to_pay=10.0
        )
        self.payment2 = Payment.objects.create(
            status=Payment.StatusChoices.PAID,
            payment_type=Payment.TypeChoices.FINE,
            borrowing_id=2,
            session_url="http://example.com",
            session_id=456,
            money_to_pay=20.0
        )

        self.user = User.objects.create_user(username='testuser', password='password123')

        self.factory = APIRequestFactory()

    def test_list_payments_authenticated(self):
        request = self.factory.get('/payments/')
        force_authenticate(request, user=self.user)

        view = PaymentViewSet.as_view({'get': 'list'})
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = PaymentSerializer([self.payment1, self.payment2], many=True).data
        self.assertEqual(response.data, expected_data)

