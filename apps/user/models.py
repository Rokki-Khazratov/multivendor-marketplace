# app name - user

from django.db import models

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver





class Favorites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    favorite_products = models.ManyToManyField('product.Product', blank=True)

    def add_to_favorites(self, product):
        self.favorite_products.add(product)

    def remove_from_favorites(self, product):
        self.favorite_products.remove(product)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100,null=True, blank=True)
    phone_number = models.CharField(max_length=15,null=True, blank=True)

    def __str__(self):
        return str(self.user) 

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()






def review_image_path(instance, filename):
    return f'review_images/{instance.review.product.id}/review_{instance.review.user.username}/{filename}'


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE,related_name='products')
    info = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        from apps.product.models import Product  # Import inside the method
        super(Review, self).save(*args, **kwargs)

        if self.product:
            self.product.reviews.add(self)

    def __str__(self):
        return f"Review by {self.user.username} : {self.rating}"

class ReviewImage(models.Model):
    review = models.ForeignKey(Review, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=review_image_path)

    def __str__(self):
        return f"Image for  {self.review}"