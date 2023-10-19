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
    quantity = models.PositiveIntegerField()
    characteristics = models.ManyToManyField(ProductCharacteristic)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Calculate the total quantity based on characteristics
        total_quantity = sum(characteristic.quantity for characteristic in self.characteristics.all())
        self.quantity = total_quantity

        super(Product, self).save(*args, **kwargs)

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
    items = models.ManyToManyField('Product', through='CartItem')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_price(self):
        total = self.items.aggregate(total_price=Sum(F('items__quantity') * F('items__product__price')))['total_price']
        return total if total is not None else 0

    def __str__(self):
        return f"Cart for {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    characteristics = models.ManyToManyField(ProductCharacteristic)

    def __str__(self):
        return f"Cart Item for Cart {self.cart.id}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    shipping_address = models.TextField()
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order by {self.user.username}"

    @staticmethod
    def create_order_from_cart(cart, shipping_address):
        order = Order.objects.create(user=cart.user, cart=cart, shipping_address=shipping_address)
        
        for cart_item in cart.cartitem_set.all():
            order_item = OrderItem(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity
            )
            order_item.save()
        
        return order

class OrderItem(models.Model) :
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    characteristics = models.ManyToManyField(ProductCharacteristic)

    def get_total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"Order Item for Order {self.order.id}"





