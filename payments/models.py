from django.core.exceptions import ValidationError
from django.db import models


class Payment(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = "PENDING"
        PAID = "PAID"

    class TypeChoices(models.TextChoices):
        PAYMENT = "PAYMENT"
        FINE = "FINE"

    status = models.CharField(
        max_length=10,
        choices=StatusChoices.choices,
    )
    payment_type = models.CharField(
        max_length=10,
        choices=TypeChoices.choices,
    )
    borrowing_id = models.IntegerField()
    session_url = models.URLField()
    session_id = models.IntegerField()
    money_to_pay = models.DecimalField(max_digits=10, decimal_places=2)

    def clean(self):
        if self.money_to_pay < 0:
            raise ValidationError("Money to pay  must be a non-negative integer.")

    def __str__(self):
        return f"Borrowing ID: {self.borrowing_id}, Status: {self.status}, Type: {self.payment_type}"
