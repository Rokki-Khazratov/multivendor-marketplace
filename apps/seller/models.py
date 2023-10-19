from django.db import models
from django.contrib.auth.models import User


class Seller(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller_profile')
    store_name = models.CharField(max_length=255,blank=True, null=True)
    address = models.CharField(max_length=255,blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True, default='+998')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.store_name
    
class SellerApplication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller_applications')
    status = models.CharField(max_length=20, choices=(('pending', 'Ожидание'), ('approved', 'Одобрено'), ('rejected', 'Отклонено')))
    store_name = models.CharField(max_length=255) 
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.user.username}:{self.store_name}"