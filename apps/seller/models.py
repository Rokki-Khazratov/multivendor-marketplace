from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


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
    
class SellerApplication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=(('pending', 'Ожидание'), ('approved', 'Одобрено'), ('rejected', 'Отклонено')))
    
    store_name = models.CharField(max_length=255) 
    address = models.CharField(max_length=255) 
    # inn = models.CharField(max_length=12) 
    # phone_number = models.CharField(max_length=15) 


@receiver(post_save, sender=SellerApplication)
def create_seller_profile(sender, instance, created, **kwargs):
    if instance.status == 'approved' and created:
        Seller.objects.create(user=instance.user)

@receiver(post_save, sender=SellerApplication)
def save_seller_profile(sender, instance, **kwargs):
    if instance.status == 'approved':
        instance.user.seller.save()