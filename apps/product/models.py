from django.db import models
from apps.seller.models import Seller
from django.contrib.auth.models import User
from django.db.models import F, Sum


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    
class ProductCharacteristic(models.Model):
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name}: {self.value} - {self.quantity}"
        

#! Product's things ----------------------------
class Product(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    handle = models.SlugField(unique=True) 
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2)
    characteristics = models.ManyToManyField(ProductCharacteristic)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')


class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    @property
    def total_price(self):
        total = 0
        for cart_item in self.cartitem_set.all():
            product_price = cart_item.product.price
            quantity = cart_item.quantity

            # Учтите характеристики
            for characteristic in cart_item.characteristics.all():
                product_price += characteristic.price  # Предположим, что у характеристики есть поле "price"
            
            total += product_price * quantity
        
        return total

    def __str__(self):
        return f"{self.user.username}'s cart"

class CharacteristicQuantity(models.Model):
    cart_item = models.ForeignKey('CartItem', on_delete=models.CASCADE)
    characteristic = models.ForeignKey(ProductCharacteristic, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.cart_item} - {self.characteristic.name} : {self.quantity}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    characteristic_quantity = models.ForeignKey(CharacteristicQuantity, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"Cart Item for Cart {self.cart.id}"   
    

    

    








