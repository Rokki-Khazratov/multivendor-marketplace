from django.contrib import admin

from apps.user.models import Review, ReviewImage
from .models import *
from .models import CartItem, CharacteristicQuantity

class CharacteristicQuantityAdmin(admin.TabularInline):
    model = CharacteristicQuantity
    extra = 1 

class CartItemAdmin(admin.ModelAdmin):
    inlines = [CharacteristicQuantityAdmin]
admin.site.register(CartItem, CartItemAdmin)


class CharacteristicImageAdmin (admin.StackedInline):
    model = CharacteristicImage


@admin.register(ProductCharacteristic)
class ProductCharacteristicAdmin(admin.ModelAdmin):
    inlines = [CharacteristicImageAdmin]
    list_display = ['name','id','value']

    class Meta:
        model = ProductCharacteristic

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','id', 'is_published', 'category']
    list_filter = ['category',]
    search_fields = ['name', 'category__name']
    # exclude = ['handle']
    prepopulated_fields = {'handle': ('name',)}
    list_per_page = 20

    class Meta:
        model = Product

@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ['store_name','id', 'phone_number']
    # list_filter = ['category']
    search_fields = ['name', 'phone_number']
    # exclude = ['handle']
    list_per_page = 20

    class Meta:
        model = Seller


admin.site.register(ParentCategory)
admin.site.register(Category)
admin.site.register(CharacteristicQuantity)
admin.site.register(Cart)




class ReviewImageAdmin (admin.StackedInline):
    model = ReviewImage

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    inlines = [ReviewImageAdmin]
    list_display = ['user','id','rating']

    class Meta:
        model = Review