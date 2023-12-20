from django.contrib import admin
from mainapp.models import Brand, Product, Cart, Order,OrderedProduct

# Register your models here.

admin.site.register(Brand)
admin.site.register(Product)

admin.site.register(Cart)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_filter = ("name",)
    ordering = ("completed",)

@admin.register(OrderedProduct)
class OrderedProductAdmin(admin.ModelAdmin):
    ordering = ("order__completed",)