from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from userapp.views import main, registration, profile, order, add_to_cart, remove_from_cart, add_to_cart_btn, make_order, suggest_address, add_to_favourite, order_history, logout, thanks_for_order, email_verif, EmailVerificationView

app_name = 'userapp'

urlpatterns = [
    path('', main, name='main'),
    path('registration/', registration, name='registration'),
    path('profile/', profile, name='profile'),
    path('order/', order, name='order'),
    path('add-to-cart/<int:product_id>', add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:cart_id>', remove_from_cart, name='remove_from_cart'),
    path('add-to-cart-btn/<int:cart_id>', add_to_cart_btn, name='add_to_cart_btn'),
    path('order/make-order', make_order, name='make-order'),
    path('order/suggest-address', suggest_address, name='suggest_address'),
    path('add-to-favourite/<int:product_id>', add_to_favourite, name='add_to_favourite'),
    path('order-history/', order_history, name='order_history'),
    path('logout/', logout, name='logout'),
    path('thanks-for-order/', thanks_for_order, name='thanks_for_order'),
    path('email-verif/<str:email>/<uuid:key>/', EmailVerificationView.as_view(), name='email_verif'),
    path('test_cbv', EmailVerificationView.as_view())
]