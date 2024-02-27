from datetime import date, timedelta

from django.test import TestCase

from borrowings.models import Borrowing


class BorrowingModelTestCase(TestCase):
    def test_successful_borrowing_creation(self):
        borrowing = Borrowing.objects.create(
            borrow_date=date.today(),
            expected_return_date=date.today() + timedelta(days=7),
            actual_return_date=None,
            book_id=1,
            user_id=1
        )
        self.assertIsNotNone(borrowing)
