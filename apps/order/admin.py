# admin.py
from django.contrib import admin
from .models import Order, OrderItem, OrderHistory, OneClickOrder, OneClickOrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

class OneClickOrderItemInline(admin.TabularInline):
    model = OneClickOrderItem
    extra = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_profile', 'created_at', 'status', 'is_paid', 'display_total_price')
    list_filter = ('status', 'is_paid')
    search_fields = ('user_profile__user__username', 'user_profile__user__email')
    inlines = [OrderItemInline]

@admin.register(OrderHistory)
class OrderHistoryAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'orders_count')
    search_fields = ('user_profile__user__username', 'user_profile__user__email')

    def orders_count(self, obj):
        return obj.orders.count()
    orders_count.short_description = 'Number of Orders'

@admin.register(OneClickOrder)
class OneClickOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'created_at', 'status')
    list_filter = ('status',)
    search_fields = ('full_name', 'email', 'phone_number')
    inlines = [OneClickOrderItemInline]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'characteristic', 'quantity', 'display_item_price')
    search_fields = ('order__id', 'characteristic__name')

    @admin.display(description='Item Price')
    def display_item_price(self, obj):
        return obj.display_item_price

    def get_inline_instances(self, request, obj=None):
        return []

