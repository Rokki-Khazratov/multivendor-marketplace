from django.contrib import admin
from .models import *


class ProductImageAdmin (admin.StackedInline):
    model = ProductImage

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageAdmin]
    list_display = ['name','id', 'price', 'quantity', 'is_published', 'category']
    list_filter = ['category',]
    search_fields = ['name', 'category__name']
    # exclude = ['handle']
    prepopulated_fields = {'handle': ('name',)}
    list_per_page = 20

    class Meta:
        model = Product

@admin.register(ProductCharacteristic)
class ProductCharacteristicAdmin(admin.ModelAdmin):
    list_display = ['name','id','value','quantity']

    class Meta:
        model = ProductCharacteristic


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ['store_name','id', 'phone_number']
    # list_filter = ['category']
    search_fields = ['name', 'phone_number']
    # exclude = ['handle']
    list_per_page = 20

    class Meta:
        model = Seller


admin.site.register(Category)