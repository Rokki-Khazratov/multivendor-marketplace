import time
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from django.db.models import F, Sum
from apps.product.models import CartItem, CharacteristicQuantity
from .models import Seller, SellerApplication


@receiver(post_save, sender=SellerApplication)
def create_or_update_seller_profile(sender, instance, created, **kwargs):
    if instance.status == 'approved':
        seller, _ = Seller.objects.get_or_create(user=instance.user)
        seller.store_name = instance.store_name
        seller.address = instance.address
        seller.phone_number = instance.phone_number
        seller.save()
        print(f"Seller created/updated: {seller}")
    elif instance.status == 'pending':
        seller, _ = Seller.objects.get_or_create(user=instance.user)
        seller.save()

@receiver(post_save, sender=SellerApplication)
def handle_seller_application_status(sender, instance, **kwargs):
    if instance.status_changed:
        seller, _ = Seller.objects.get_or_create(user=instance.user)
        if instance.status == 'approved':
            time.sleep(10)
            instance.delete()
        elif instance.status == 'rejected':
            seller.delete()
            instance.delete()

@receiver(post_save, sender=CharacteristicQuantity)
def update_cart_item(sender, instance, created, **kwargs):
    cart_item = instance.cart_item
   
    cart_item.quantity = instance.quantity
    cart_item.characteristic_quantity = instance 
    cart_item.save()




