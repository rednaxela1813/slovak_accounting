from django.contrib import admin
from .models import Product, Order



class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price')
    search_fields = ('name',)
    list_filter = ('price',)
    
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'updated_at', 'total_price', 'status')
    search_fields = ('status',)
    list_filter = ('status', 'created_at', 'updated_at')
    
    
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)

