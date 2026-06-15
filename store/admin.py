from django.contrib import admin
from .models import Product, Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'full_name',
        'phone_number',
        'total_amount',
        'status',
        'created_at'
    )

    search_fields = (
        'full_name',
        'phone_number'
    )

    list_filter = (
        'created_at',
        'status',
    )

    inlines = [OrderItemInline]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')