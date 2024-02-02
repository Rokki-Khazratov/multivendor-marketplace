# #!-----------------ORDER VIA user_profile----------------
# class Order(models.Model):
#     user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     # updated_at = models.DateTimeField(auto_now=True)

#     status = models.IntegerField(choices=STATUS_CHOICES, default=PENDING)
#     is_paid = models.BooleanField(default=False)
#     # payment_method = models.CharField(max_length=255, null=True, blank=True)
#     # shipping_address = models.TextField(null=True, blank=True)


#     @property
#     def display_total_price(self):
#         return sum(item.display_item_price * item.quantity for item in self.order_items.all())


#     def __str__(self):
#         return f"Order {self.id} - {self.user_profile.user.username if self.user_profile else 'Guest'}"


# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
#     characteristic = models.ForeignKey(ProductCharacteristic, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField()

#     @property
#     def display_item_price(self):
#         return self.characteristic.price

#     def __str__(self):
#         return f"{self.order} - {self.characteristic.name} : {self.quantity}"

# class OrderHistory(models.Model):
#     user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
#     orders = models.ManyToManyField(Order, related_name='order_history')

#     def __str__(self):
#         return f"OrderHistory for {self.user_profile.user.username} - {self.orders.count()} Orders"
    
# #!-----------------ORDER IN ONE CLICK----------------
# class OneClickOrder(models.Model):
#     created_at = models.DateTimeField(auto_now_add=True)
#     status = models.IntegerField(choices=STATUS_CHOICES, default=PENDING)


#     full_name = models.CharField(max_length=255)
#     email = models.EmailField(null=True)
#     phone_number = models.CharField(max_length=15)
#     address = models.TextField()

#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)


#     def __str__(self):
#         return f"One-Click Order {self.id} - {self.full_name}"

# class OneClickOrderItem(models.Model):
#     order = models.ForeignKey(OneClickOrder, on_delete=models.CASCADE, related_name='items')
#     characteristic = models.ForeignKey(ProductCharacteristic, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField()

#     @property
#     def display_item_price(self):
#         return self.characteristic.price

#     def __str__(self):
#         return f"One-Click Order {self.order.id} Item - {self.characteristic.name} : {self.quantity}"

# #! ----signals----
# @receiver(post_save, sender=Order)
# def move_order_to_history(sender, instance, **kwargs):
#     if instance.status == Order.GOTTED:
#         OrderHistory.objects.create(user_profile=instance.user_profile, order=instance)









# models.py
from django.db import models
from apps.product.models import ProductCharacteristic
from apps.user.models import UserProfile

#signals:
from django.db.models.signals import post_save
from django.dispatch import receiver






#* status of order
PENDING = 1
PROCESSING = 2
DELIVERED = 3
GOTTED = 4

STATUS_CHOICES = [
    (PENDING, 'В ожидании'), #orange
    (PROCESSING, 'В пути'), #yellow
    (DELIVERED, 'Доставлен и ожидает'), #GREEN !!!!
    (GOTTED, 'Забран'), #gray
]



class Order(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    status = models.IntegerField(choices=STATUS_CHOICES, default=PENDING)
    is_paid = models.BooleanField(default=False)
    shipping_address = models.TextField(null=True, blank=True)


    @property
    def display_total_price(self):
        return sum(item.display_item_price * item.quantity for item in self.order_items.all())


    def __str__(self):
        return f"Order {self.id} - {self.user_profile.user.username if self.user_profile else 'Guest'}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    characteristic = models.ForeignKey(ProductCharacteristic, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    @property
    def display_item_price(self):
        return self.characteristic.price

    def __str__(self):
        return f"{self.order} - {self.characteristic.name} : {self.quantity}"

class OrderHistory(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    orders = models.ManyToManyField(Order, related_name='order_history')

    def __str__(self):
        return f"OrderHistory for {self.user_profile.user.username} - {self.orders.count()} Orders"