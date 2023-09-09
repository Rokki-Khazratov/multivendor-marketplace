from django.db import models
from django.contrib.auth.models import AbstractUser

# class CustomUser(AbstractUser):
#     USER_TYPE_CHOICES = (
#         ('buyer', 'Buyer'),
#         ('seller', 'Seller'),
#         ('staff', 'Staff'),
#     )
#     user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='buyer')

#     def is_buyer(self):
#         return self.user_type == 'buyer'

#     def is_seller(self):
#         return self.user_type == 'seller'

#     def is_staff(self):
#         return self.user_type == 'staff'



class Seller(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name




#! Product's things ----------------------------
class Product(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    handle = models.SlugField(unique=True) # slug
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def add_to_cart(self, user):
        cart_item, created = CartItem.objects.get_or_create(product=self, user=user)
        if not created:
            cart_item.quantity += 1
            cart_item.save()

    def remove_from_cart(self, user):
        try:
            cart_item = CartItem.objects.get(product=self, user=user)
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()
        except CartItem.DoesNotExist:
            pass


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')

class ProductCharacteristic(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    # user = models.ForeignKey(Seller, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    # user = models.ForeignKey(Seller, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

#! ----------------------------


 



class Order(models.Model):
    # user = models.ForeignKey(Seller, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderItem')
    created_at = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()