from django.db import models
from apps.seller.models import Seller
from django.contrib.auth.models import User
from django.db.models import F, Sum
from django.core.validators import MinValueValidator, MaxValueValidator

from apps.user.models import UserProfile

# from apps.user.models import Review





# def characteristic_image_path(instance, filename):
#     return f'products/{instance.characteristic.product.seller.store_name}-{instance.characteristic.product.id}/{filename}'
def characteristic_image_path(instance, filename):
    product = instance.characteristic.product
    return f'products/{product.seller.store_name}-{product.id}/{filename}'




class ParentCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey(ParentCategory, null=True, blank=True,on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name



        

#! Product's things ----------------------------
class Product(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, null=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    handle = models.SlugField(unique=True) 
    reviews = models.ManyToManyField('user.Review', related_name='products', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    @property
    def display_seller_name(self):
        return self.seller.store_name
    
    # def save(self, *args, **kwargs):
    #     if self.reviews.count() > 0:
    #         total_rating = sum(review.rating for review in self.reviews.all())
    #         self.rating = total_rating / self.reviews.count()
    #     else:
    #         self.rating = 0.0

    #     super(Product, self).save(*args, **kwargs)

    
class ProductCharacteristic(models.Model):
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(null=True, blank=True)
    images = models.ManyToManyField('CharacteristicImage', related_name='product_characteristics', blank=True)

    def __str__(self):
        return f"{self.name}: {self.value}"


class CharacteristicImage(models.Model):
    characteristic = models.ForeignKey(ProductCharacteristic, related_name='characteristic_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=characteristic_image_path,max_length=500)

    def __str__(self):
        return f"Image for {self.characteristic.name}"













class CharacteristicQuantity(models.Model):
    cart_item = models.ForeignKey('CartItem', on_delete=models.CASCADE)
    characteristic = models.ForeignKey(ProductCharacteristic, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.cart_item} - {self.characteristic.name} : {self.quantity}"







class CartItem(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    characteristics = models.ManyToManyField(ProductCharacteristic, through='CharacteristicQuantity')

    def __str__(self):
        return f"Cart Item for Cart {self.user_profile.id}"   