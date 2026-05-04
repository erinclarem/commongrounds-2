from django.contrib import admin
from .models import Product, ProductType, Transaction


class ProductInline(admin.TabularInline):
    model = Product


class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ['name', 'product_type', 'price', 'stock', 'status', 'owner']


class ProductTypeAdmin(admin.ModelAdmin):
    model = ProductType
    inlines = [ProductInline,]


class TransactionAdmin(admin.ModelAdmin):
    model = Transaction
    list_display = ['product', 'buyer', 'amount', 'status', 'created_on']


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(Transaction, TransactionAdmin)
