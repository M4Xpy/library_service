from django.core.exceptions import ValidationError
from django.db import models


class Book(models.Model):
    class CoverChoices(models.TextChoices):
        HARD = "HARD"
        SOFT = "SOFT"

    title = models.CharField(
        max_length=255,
    )
    author = models.CharField(
        max_length=255,
    )
    cover = models.CharField(
        max_length=4,
        choices=CoverChoices.choices,
    )
    inventory = models.PositiveIntegerField(
        default=0,
    )
    daily_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    def clean(self):
        if self.inventory < 0:
            raise ValidationError("Inventory must be a non-negative integer.")
        if self.daily_fee < 0:
            raise ValidationError("Daily fee must be a non-negative decimal value.")

    def __str__(self):
        return self.title
