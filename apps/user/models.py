from django.db import models

from django.db import models
from django.contrib.auth.models import User
from apps.product.models import Product

class Favorites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    favorite_products = models.ManyToManyField(Product, blank=True)

    def add_to_favorites(self, product):
        self.favorite_products.add(product)

    def remove_from_favorites(self, product):
        self.favorite_products.remove(product)
