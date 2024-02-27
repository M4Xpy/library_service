import requests
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from books.models import Book
from borrowings.models import Borrowing
from borrowings.serializers import BorrowingSerializer
from library_service.settings import TELEGRAM_CHAT_ID, TELEGRAM_BOT_TOKEN


def send_telegram_message(message):
    requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
                  {"chat_id": TELEGRAM_CHAT_ID,
                   "text": message, },
                  )


@extend_schema(
    parameters=[
        OpenApiParameter(
            name="user id",
            type=str,
            description="Filter by user id",
            required=False,
            location="query",
        ),
        OpenApiParameter(
            name="is active",
            type=str,
            description="Filter by active borrowing",
            required=False,
            location="query",
        ),
    ],
)
class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    # permission_classes = IsAdminOrIfAuthenticatedReadOnly,

    def get_queryset(self):
        queryset = self.queryset
        user_id = self.request.query_params.get("user_id")
        is_active = self.request.query_params.get("is_active")

        if user_id:
            queryset = queryset.filter(
                user_id=user_id, )

        if is_active:
            queryset = queryset.filter(actual_return_date__isnull=int(is_active) > 0)

        return queryset.distinct()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        self.update_inventory(serializer.validated_data['book_id'], -1)
        send_telegram_message(f"Your borrowing book: "
                              f"{serializer.validated_data['book_id']}, "
                              f"return date is {serializer.validated_data['expected_return_date']}")
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        if 'actual_return_date' in serializer.validated_data:
            if instance.actual_return_date:
                raise ValidationError("This borrowing has already been returned.")
            instance.actual_return_date = serializer.validated_data['actual_return_date']
        self.perform_update(serializer)

        if instance.actual_return_date:
            self.update_inventory(instance.book_id, 1)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        self.update_inventory(instance.book_id, 1)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def update_inventory(book_id, change):
        try:
            book = Book.objects.get(pk=book_id)
            book.inventory += change
            book.save()
        except Book.DoesNotExist:
            pass
