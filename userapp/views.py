from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from userapp.forms import UserRegistrationForm, UserProfileForm
from mainapp.models import Product, Cart
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
    return HttpResponse('1')

def add_to_cart(request, product_id):
    user = request.user
    product = Product.objects.get(id=product_id)
    cart = Cart.objects.filter(product=product, user=user)
    if cart.exists():
        cart = cart.first()
        cart.quantity += 1
        cart.save()
    else:
        cart = Cart.objects.create(product=product, user=user)
        cart.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])

def cart(request):
    user = request.user
    carts = Cart.objects.filter(user=user.id)
    return carts

def remove_from_cart(request,cart_id):
    user = request.user
    cart = Cart.objects.get(id=cart_id)
    cart.quantity -= 1
    cart_quantity = cart.quantity
    if cart.quantity <= 0:
        cart.delete()
    else:
        cart.save()
    return JsonResponse({'new_quantity':cart_quantity})

    
