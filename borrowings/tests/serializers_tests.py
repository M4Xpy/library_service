from datetime import date, timedelta

from django.test import TestCase

from borrowings.models import Borrowing
from borrowings.serializers import BorrowingSerializer


class BorrowingSerializerTestCase(TestCase):
    def test_serializer_data(self):
        borrowing = Borrowing.objects.create(
            borrow_date=date.today(),
            expected_return_date=date.today() + timedelta(days=7),
            actual_return_date=None,
            book_id=1,
            user_id=1
        )
        serializer = BorrowingSerializer(borrowing)

        expected_data = {
            "id": borrowing.id,
            "book_id": 1,
            "user_id": 1,
            "borrow_date": str(borrowing.borrow_date),
            "expected_return_date": str(borrowing.expected_return_date),
            "actual_return_date": borrowing.actual_return_date,
        }
        self.assertEqual(serializer.data, expected_data)
