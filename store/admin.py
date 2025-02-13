from django.contrib import admin
from .models import Product, Cart, Order, OrderItem, Category

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'category')
    search_fields = ('name', 'category')
    list_filter = ('category',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'image')  # Show these fields in the list view
    search_fields = ('name',)  # Enable search by category name

# Register Category with the custom CategoryAdmin
admin.site.register(Category, CategoryAdmin)

# Register Product with the custom ProductAdmin
admin.site.register(Product, ProductAdmin)

# Register other models
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItem)
