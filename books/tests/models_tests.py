from django.core.exceptions import ValidationError
from django.test import TestCase

from books.models import Book


class BookModelTestCase(TestCase):
    def test_clean_method_with_negative_inventory(self):
        book = Book(
            title="Test Book",
            author="Test Author",
            cover="HARD",
            inventory=-1,
            daily_fee=10.0,
        )

        with self.assertRaises(ValidationError) as cm:
            book.clean()

        self.assertEqual(
            cm.exception.message, "Inventory must be a non-negative integer."
        )

    def test_clean_method_with_negative_daily_fee(self):
        book = Book(
            title="Test Book",
            author="Test Author",
            cover="HARD",
            inventory=10,
            daily_fee=-1.0,
        )

        with self.assertRaises(ValidationError) as cm:
            book.clean()

        self.assertEqual(
            cm.exception.message, "Daily fee must be a non-negative decimal value."
        )

    def test_clean_method_with_valid_data(self):
        book = Book(
            title="Test Book",
            author="Test Author",
            cover="HARD",
            inventory=10,
            daily_fee=10.0,
        )
        book.clean()
