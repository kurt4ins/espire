from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from userapp.forms import UserRegistrationForm, UserProfileForm
from userapp.models import User
import uuid
from mainapp.models import Brand, Product, Cart, Order, OrderedProduct
from userapp.forms import UserLoginForm, OrderForm
from django.db.models import Q 
# Create your views here.


def main(request):
    return HttpResponse('1')

def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        print(form.errors)
        if form.is_valid():
            # firstname = request.POST['firstname']
            # lastname = request.POST['lastname']
            # username = request.POST['username']
            # email = request.POST['email']
            # password1 = request.POST['password1']
            # password2 = request.POST['password2']
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
            else:
                cart_info = Cart.objects.filter(device_id=request.session['device_id'], completed=0)
            for cart in cart_info:
                ordered_product = OrderedProduct.objects.create(quantity=cart.quantity, order=order_info, product=cart.product)
                ordered_product.save()
                cart.delete()
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

    