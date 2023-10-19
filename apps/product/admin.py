from django.contrib import admin
from .models import *
from .models import CartItem, CharacteristicQuantity

# Определите административную модель для CharacteristicQuantity
class CharacteristicQuantityAdmin(admin.TabularInline):
    model = CharacteristicQuantity
    extra = 1  # Количество дополнительных записей для добавления

# Определите административную модель для CartItem
class CartItemAdmin(admin.ModelAdmin):
    inlines = [CharacteristicQuantityAdmin]

admin.site.register(CartItem, CartItemAdmin)

class ProductImageAdmin (admin.StackedInline):
    model = ProductImage

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageAdmin]
    list_display = ['name','id', 'price', 'is_published', 'category']
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
admin.site.register(CharacteristicQuantity)
admin.site.register(Cart)