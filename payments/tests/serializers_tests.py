from django.test import TestCase

from payments.models import Payment
from payments.serializers import PaymentSerializer


class PaymentSerializerTestCase(TestCase):
    def test_serializer_data(self):
        payment = Payment.objects.create(
            status=Payment.StatusChoices.PENDING,
            payment_type=Payment.TypeChoices.PAYMENT,
            borrowing_id=1,
            session_url="http://example.com",
            session_id=123,
            money_to_pay=10.0,
        )
        serializer = PaymentSerializer(payment)

        expected_data = {
            "id": payment.id,
            "status": Payment.StatusChoices.PENDING,
            "payment_type": Payment.TypeChoices.PAYMENT,
            "borrowing_id": 1,
            "session_url": "http://example.com",
            "session_id": 123,
            "money_to_pay": "10.00",
        }
        self.assertEqual(serializer.data, expected_data)
