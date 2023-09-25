from django.db import models
from django.contrib.auth.models import User



class Seller(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name