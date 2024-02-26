from django.db import models


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True, )
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True, )
    book_id = models.IntegerField()
    user_id = models.IntegerField()

    def __str__(self):
        return f"Borrowing ID: {self.id}"
