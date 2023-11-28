from django.db import models
from django.contrib.auth.models import User
from apps.product.models import  Product, ProductCharacteristic


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
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

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    characteristics = models.ManyToManyField(ProductCharacteristic)

    def get_total_price(self):
        return self.product.price * self.quantity

    @property
    def total_characteristics_quantity(self):
        return sum(characteristic.quantity for characteristic in self.characteristics.all())

    def __str__(self):
        return f"Order Item for Order {self.order.id}"