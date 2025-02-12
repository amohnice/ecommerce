from django.contrib import admin
from .models import Product, Cart, Order, OrderItem

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'category')
    search_fields = ('name', 'category')
    list_filter = ('category',)

# Register Product with the custom ProductAdmin
admin.site.register(Product, ProductAdmin)

# Register other models
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItem)
