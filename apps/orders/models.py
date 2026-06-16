from django.db import models
from django.contrib.auth import get_user_model

User=get_user_model()

class Address(models.Model):
    class AddressType(models.TextChoices):
        HOME = "Home", "Home"
        WORK = "Work", "Work"
        SCHOOL = "School", "School"
        OTHER = "Other", "Other"

    user=models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="addresses"
    )

    address_type=models.CharField(
        max_length=15,
        choices=AddressType.choices,
        default=AddressType.HOME
    )

    full_name=models.CharField(max_length=100)
    phone_number=models.CharField(max_length=15)

    address_line1=models.CharField(max_length=255)
    address_line1=models.CharField(
        max_length=255,
        blank=True,
    )

    city=models.CharField(max_length=100)
    state=models.CharField(max_length=100)

    postal_code=models.CharField(max_length=20)

    country=models.CharField(max_length=100)

    is_default=models.BooleanField(default=False)

    created_at=models.DateTimeField(auto_now_add=True)


    class Meta:
        db_table="addresses"
        ordering=["-created_at"]

    def __str__(self):
        return f"{self.full_name}- {self.get_address_type_display()}"