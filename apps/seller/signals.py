from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Seller, SellerApplication

@receiver(post_save, sender=SellerApplication)
def create_seller_profile(sender, instance, created, **kwargs):
    if instance.status == 'approved':
        seller, _ = Seller.objects.get_or_create(user=instance.user)
        seller.store_name = instance.store_name
        seller.address = instance.address
        seller.phone_number = instance.phone_number
        seller.save()
    elif instance.status == 'pending' and created:
        seller, _ = Seller.objects.get_or_create(user=instance.user)
        seller.save()

@receiver(post_save, sender=SellerApplication)
def save_seller_profile(sender, instance, **kwargs):
    if instance.status == 'approved':
        seller, created = Seller.objects.get_or_create(user=instance.user)
        seller.save()
