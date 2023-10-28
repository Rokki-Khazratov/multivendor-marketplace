from django.db import models
from apps.seller.models import Seller
from django.contrib.auth.models import User
from django.db.models import F, Sum
from django.core.validators import MinValueValidator, MaxValueValidator

# from apps.user.models import Review


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    


        

#! Product's things ----------------------------
class Product(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    handle = models.SlugField(unique=True) 
    reviews = models.ManyToManyField('user.Review', related_name='products', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.reviews.count() > 0:
            total_rating = sum(review.rating for review in self.reviews.all())
            self.rating = total_rating / self.reviews.count()
        else:
            self.rating = 0.0

        super(Product, self).save(*args, **kwargs)

    def get_price(self):
        price = ProductCharacteristic.get_price(ProductCharacteristic)
        return price

class ProductCharacteristic(models.Model):
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.name}: {self.value}"
    
    def get_price(self):
        price = self.price
        return price

class CharacteristicImage(models.Model):
    characteristic = models.ForeignKey(ProductCharacteristic, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')
    characteristic = models.ForeignKey(ProductCharacteristic, on_delete=models.CASCADE)

    def __str__(self):
        return f"Image for  {self.characteristic.name}"

class CharacteristicQuantity(models.Model):
    cart_item = models.ForeignKey('CartItem', on_delete=models.CASCADE)
    characteristic = models.ForeignKey(ProductCharacteristic, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.cart_item} - {self.characteristic.name} : {self.quantity}"








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

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    characteristic_quantity = models.ForeignKey(CharacteristicQuantity, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"Cart Item for Cart {self.cart.id}"   