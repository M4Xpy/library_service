from django.test import TestCase

from books.models import Book
from books.serializers import BookSerializer


class BookSerializerTestCase(TestCase):
    def test_serializer_with_partial_data(self):
        book_data = {
            "title": "Test Book",
            "author": "Test Author",
            "cover": "HARD",
            "daily_fee": "10.00",
        }
        book = Book.objects.create(**book_data)

        serializer = BookSerializer(book)

        expected_data = {
            "id": book.id,
            "title": "Test Book",
            "author": "Test Author",
            "cover": "HARD",
            "inventory": 0,
            "daily_fee": "10.00",
        }
        self.assertEqual(serializer.data, expected_data)
