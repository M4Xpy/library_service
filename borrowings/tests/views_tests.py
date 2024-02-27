from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from books.models import Book
from borrowings.models import Borrowing
from borrowings.views import BorrowingViewSet


class BorrowingViewSetTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.book = Book.objects.create(title='Test Book', author='Test Author', inventory=1, daily_fee=1.0)

    def test_create_borrowing(self):
        request = self.factory.post('/borrowings/', {
            'borrow_date': '2024-02-27',
            'expected_return_date': '2024-03-05',
            'book_id': self.book.id,
            'user_id': self.user.id
        })
        force_authenticate(request, user=self.user)

        with patch('borrowings.views.send_telegram_message') as mock_send_telegram_message:
            response = BorrowingViewSet.as_view({'post': 'create'})(request)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            mock_send_telegram_message.assert_called_once()

    def test_destroy_borrowing(self):
        borrowing = Borrowing.objects.create(
            borrow_date='2024-02-27',
            expected_return_date='2024-03-05',
            book_id=self.book.id,
            user_id=self.user.id
        )
        request = self.factory.delete(f'/borrowings/{borrowing.id}/')
        force_authenticate(request, user=self.user)

        with patch('borrowings.views.BorrowingViewSet.update_inventory') as mock_update_inventory:
            response = BorrowingViewSet.as_view({'delete': 'destroy'})(request, pk=borrowing.id)
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
            mock_update_inventory.assert_called_once_with(self.book.id, 1)
