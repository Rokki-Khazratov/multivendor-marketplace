# app name - seller

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def validate_seller_name(value):
    invalid_chars = set("!'\"@#$%^&*()_+=<>?{}[]|\\;:,~`" and " ")
    if any(char in invalid_chars for char in value):
        raise ValidationError("Invalid character in seller name")

class SellerBaseModel(models.Model):
    store_name = models.CharField(max_length=255, unique=True, null=True, validators=[validate_seller_name])
    address = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        abstract = True


class Seller(SellerBaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller_profile')
    PREMIUM_TARIFF_CHOICES = [
        (1, 'Basic'),
        (2, 'Standard'),
        (3, 'Premium'),
    ]
    premium_tariff = models.IntegerField(choices=PREMIUM_TARIFF_CHOICES, default=1)
    avatarka = models.ImageField(upload_to="sellers_avatarka/",blank=True, null=True)
    background = models.ImageField(upload_to="sellers_background/",blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self): 
        return self.store_name


class SellerApplication(SellerBaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller_applications')
    status = models.CharField(
        max_length=20, choices=(('pending', 'Ожидание'), ('approved', 'Одобрено'), ('rejected', 'Отклонено'))
    )
    status_changed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}:{self.store_name}"

    def save(self, *args, **kwargs):
        if self.status == 'approved' or self.status == 'rejected':
            self.status_changed = True
        super(SellerApplication, self).save(*args, **kwargs)