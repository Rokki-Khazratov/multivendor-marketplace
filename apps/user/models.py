from django.db import models

from django.db import models
from django.contrib.auth.models import User
from apps.product.models import Product
from django.core.validators import MinValueValidator, MaxValueValidator

class Favorites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    favorite_products = models.ManyToManyField(Product, blank=True)

    def add_to_favorites(self, product):
        self.favorite_products.add(product)

    def remove_from_favorites(self, product):
        self.favorite_products.remove(product)




class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    info = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} : {self.rating}"

    def save(self, *args, **kwargs):
        super(Review, self).save(*args, **kwargs)

class ReviewImage(models.Model):
    review = models.ForeignKey(Review, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='review_images/')

    def __str__(self):
        return f"Image for  {self.user.id}"