from django.contrib import admin
from mainapp.models import Brand, Product,Cart

# Register your models here.

admin.site.register(Brand)
admin.site.register(Product)

admin.site.register(Cart)