from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from userapp.views import main, registration, profile, order, add_to_cart, remove_from_cart

app_name = 'userapp'

urlpatterns = [
    path('', main, name='main'),
    path('registration/', registration, name='registration'),
    path('profile/', profile, name='profile'),
    path('order/', order, name='order'),
    path('add_to_cart/<int:product_id>', add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:cart_id>', remove_from_cart, name='remove_from_cart')
]