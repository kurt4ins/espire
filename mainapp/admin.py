from django.contrib import admin
from mainapp.models import Brand, Product, Cart, Order, OrderedProduct, User

# Register your models here.

admin.site.register(Brand)
admin.site.register(Product)

admin.site.register(Cart)
admin.site.register(User)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_filter = ("name",)
    ordering = ("completed",)

@admin.register(OrderedProduct)
class OrderedProductAdmin(admin.ModelAdmin):
    ordering = ("order__completed",)