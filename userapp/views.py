from django.db.models.query import QuerySet
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from userapp.forms import UserRegistrationForm, UserProfileForm
from userapp.models import User, EmailVerification
import uuid
from mainapp.models import Brand, Product, Cart, Order, OrderedProduct, Favourite
from userapp.forms import UserLoginForm, OrderForm
from django.db.models import Q
from django.urls import reverse
from django.contrib import auth
import requests
from pprint import pprint
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from common.views import TitleMixin
from yookassa import Configuration, Payment
import os
from dotenv import load_dotenv
import json
# Create your views here.
load_dotenv()

def main(request):
    return HttpResponse('1')

def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        print(form.errors)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = UserRegistrationForm()
    context = {'form':form}
    return render(request, 'userapp/registration.html', context)

def profile(request):
    if request.method == 'GET':
        form = UserProfileForm(instance=request.user)
    else:
        form = UserProfileForm(data=request.POST, instance=request.user)
        
        if form.is_valid():
            form.save()
    context = {'form':form}
    return render(request, 'userapp/profile.html', context)

def get_payment(request):
    Configuration.account_id = os.getenv('SHOP_ID')
    Configuration.secret_key = os.getenv('YOOKASSA_SECRET')
    payment_id = str(uuid.uuid4())
    payment = Payment.create({
        "amount": {
            "value": "100.00",
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": 'http://localhost:8000'+reverse('userapp:thanks_for_order', kwargs={'payment_id':payment_id})
        },
        "capture": True,
        "description": "Заказ №1"
    }, payment_id)

    return payment

def order(request):
    user = request.user
    if request.method == 'POST':
        errors = True
        order = OrderForm(request.POST)
        if order.is_valid():
            # print(order.cleaned_data)
            order.save() 
            order_info = Order.objects.last()
            if user.id:
                cart_info = Cart.objects.filter(user = user, completed=0)
                order_info.is_user = 1
                order_info.user = user
                order_info.save()
            else:
                cart_info = Cart.objects.filter(device_id=request.session['device_id'], completed=0)
            for cart in cart_info:
                ordered_product = OrderedProduct.objects.create(quantity=cart.quantity, order=order_info, product=cart.product)
                ordered_product.save()
                cart.delete()
            #print(payment(request).json())
            payment = json.loads(get_payment(request).json())
            order_info.payment_id = payment['id']
            order_info.save()
            return HttpResponseRedirect(payment['confirmation']['confirmation_url'])
    else:
        if user.id == None:
            data = {}
        else:
            user_data = User.objects.get(id=user.id)
            data = {'email':user_data.email, 'name':f'{user_data.first_name} {user_data.last_name}'}
        errors = False
        order = OrderForm(data=data)
    context = {'goods':Product.objects.all(), 'brands':Brand.objects.all(), 'form':UserLoginForm, 'order_form':order, 'carts':get_cart(request), 'errors':errors}
    return render(request, 'userapp/order.html', context)

def add_to_cart(request, product_id):
    try:
        device_id = request.session['device_id']
    except KeyError:
        device_id = str(uuid.uuid4())
        request.session['device_id'] = device_id
    user = request.user
    product = Product.objects.get(id=product_id)
    if user.id == None:
        user = None
        cart = Cart.objects.filter(product=product, user=user, device_id=device_id)
    else:
        cart = Cart.objects.filter(product=product, user=user)
    if cart.exists():
        cart = cart.first()
        cart.quantity += 1
        cart.save()
    else:
        cart = Cart.objects.create(product=product, user=user, device_id=device_id)
        cart.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])

def get_total_cart_sum(request):
    try:
        device_id = request.session['device_id']
    except KeyError:
        device_id = str(uuid.uuid4())
        request.session['device_id'] = device_id
    cart = get_cart(request)[0]

    return JsonResponse({'total_sum':cart.total_sum(device_id)})

def add_to_favourite(request, product_id):
    try:
        device_id = request.session['device_id']
    except KeyError:
        device_id = str(uuid.uuid4())
        request.session['device_id'] = device_id
    user = request.user
    product = Product.objects.get(id=product_id)
    if user.id == None:
        user = None
        favourite = Favourite.objects.filter(product=product, user=user, device_id=device_id)
    else:
        favourite = Favourite.objects.filter(product=product, user=user)
    if favourite.exists():
        favourite = favourite.first()
        favourite.delete() 
    else:
        favourite = Favourite.objects.create(product=product, user=user, device_id=device_id)
        favourite.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

def get_cart(request):
    try:
        device_id = request.session['device_id']
    except KeyError:
        device_id = str(uuid.uuid4())
        request.session['device_id'] = device_id
    user = request.user
    if user.id == None:
        user = None
        carts = Cart.objects.filter(device_id=device_id, completed = False)
    else:
        carts = Cart.objects.filter(Q(user=user) | Q(device_id=device_id), completed = False)
    return carts

def get_favourite(request):
    try:
        device_id = request.session['device_id']
    except KeyError:
        device_id = str(uuid.uuid4())
        request.session['device_id'] = device_id
    user = request.user
    if user.id == None:
        user = None
        favourites = Favourite.objects.filter(device_id=device_id)
    else:
        favourites = Favourite.objects.filter(Q(user=user) | Q(device_id=device_id))
    return favourites

def remove_from_cart(request,cart_id):
    cart = Cart.objects.get(id=cart_id)
    cart.quantity -= 1
    cart_quantity = cart.quantity
    if cart.quantity <= 0:
        cart.delete()
    else:
        cart.save()
    return JsonResponse({'new_quantity':cart_quantity})

def add_to_cart_btn(request, cart_id):
    cart = Cart.objects.get(id=cart_id)
    cart.quantity += 1
    cart.save()
    return JsonResponse({'new_quantity':cart.quantity})

def make_order(request):
    order = OrderForm(request.POST)
    if order.is_valid():
        return HttpResponse('1')

def suggest_address(request):
    data = request.GET.get('data')
    ans = requests.get(f'https://suggest-maps.yandex.ru/v1/suggest?apikey=781f59c0-5f81-470b-a396-9c28b38e3fe8&text={data}&ll=37.37,55.55&types=street,house&print_address=1')
    # pprint(ans.json())
    res = {'results': [elem['address']['formatted_address']  for elem in ans.json()['results'] if elem['address']['component'][0]['name'] == 'Россия']}
    return JsonResponse(res)

def order_history(request):
    return HttpResponse('История заказов')

def logout(request):
    # return HttpResponse(1)
    auth.logout(request)
    return HttpResponseRedirect(reverse('goods'))

def thanks_for_order(request, payment_id):
    order = Order.objects.get(payment_id=payment_id)
    order.is_paid = 1
    order.save()

    return render(request, 'userapp/thanks_for_order.html')

def email_verif(request, email, key):
    return HttpResponse('Успех')

class EmailVerificationView(TitleMixin, TemplateView):
    template_name = 'userapp/success_verif.html'
    title = 'Подтверждение email'
    
    def get(self, request, *args, **kwargs):
        key = kwargs['key']
        email = kwargs['email']
        user = User.objects.get(email=email)
        email_verif = EmailVerification.objects.filter(user=user, key=key)
        if email_verif.exists():
            user.is_verified_email = True
            user.save()
        return super(EmailVerificationView, self).get(request, *args, **kwargs)
    
    