from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from books.models import Book


class BookViewSetTestCase(TestCase):
    def setUp(self):
        self.book1 = Book.objects.create(
            title="Book 1",
            author="Author 1",
            cover="HARD",
            inventory=10,
            daily_fee=10.00,
        )
        self.book2 = Book.objects.create(
            title="Book 2", author="Author 2", cover="SOFT", inventory=5, daily_fee=8.00
        )

        self.client = APIClient()

    def test_non_admin_cannot_modify_books(self):
        # Create a regular user
        user = User.objects.create(username="user", is_staff=False, is_superuser=False)

        # Authenticate as the regular user
        self.client.force_authenticate(user=user)

        # Attempt to modify a book using PUT request
        response = self.client.put(
            f"/api/books/{self.book1.id}/", {"title": "Updated Title"}
        )

        # Verify that the request was forbidden (HTTP status code 403)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Verify that the book's title has not been updated
        self.book1.refresh_from_db()
        self.assertNotEqual(self.book1.title, "Updated Title")
