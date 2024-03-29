from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from mainapp.models import Brand, Product, Cart, Favourite
from userapp.forms import UserLoginForm
from userapp.models import User
from django.contrib import auth
from userapp.views import get_cart, get_favourite
import uuid
# Create your views here.

# def main(request):
#     context = {'goods':Product.objects.all(), 'brands':Brand.objects.all()}
#     return render(request,'mainapp/goods.html', context)

def goods(request, context=None):
    try:
        device_id = request.session['device_id']
    except KeyError:
        device_id = str(uuid.uuid4())
        request.session['device_id'] = device_id
    print(request.session['device_id'])
    if request.method == 'GET':
        if not context:
            brands = request.GET.getlist('brand')
            print(brands)
            favourites = get_favourite(request)
            id_favourites = [x.product_id for x in favourites]
            if brands:
                goods = Product.objects.filter(brand__in = brands)
            else:
                goods = Product.objects.all()
            #goods.order_by('-cost')
            context = {'goods':goods,
                       'brands':Brand.objects.all(),
                       'form':UserLoginForm, 
                       'carts':get_cart(request),
                       'favourites':favourites, 
                       'id_favourites':id_favourites, 
                       'range':range(len(get_cart(request))),
                       'range_goods': range(len(Product.objects.all()))}
        return render(request,'mainapp/goods.html', context)
    else:
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                compare_carts(user,device_id)
        return HttpResponseRedirect('/')
        
def compare_carts(user,device_id):
    carts = Cart.objects.filter(device_id=device_id)
    for cart in carts:
        cart.user = user
        cart.save()
    carts2 = Cart.objects.filter(user=user)
    sorted_carts = carts2.order_by('product')
    i = 1
    if len(sorted_carts) > 0:
        last_product = sorted_carts[0].product
        while i < len(sorted_carts):
            if last_product == sorted_carts[i].product:
                sorted_carts[i].delete()
            else:
                last_product = sorted_carts[i].product
            i += 1
            print(sorted_carts)

def good(request):
    try:
        device_id = request.session['device_id']
    except KeyError:
        device_id = str(uuid.uuid4())
        request.session['device_id'] = device_id
    
    good_id = request.GET.get('id')
    good_info = Product.objects.get(id=good_id)
    return render(request,'mainapp/good.html',{'good':good_info, 
                                               'brands':Brand.objects.all(), 
                                               'form':UserLoginForm, 
                                               'carts':get_cart(request)})

def search(request):
    search_text = request.GET.get('search_text')
    filtered = Product.objects.filter(name__icontains=search_text)
    return goods(request, {'goods':filtered, 'brands':Brand.objects.all()})

def sort(request):
    sort_id=request.GET.get('id')
    filtered = Product.objects.filter(brand_id=sort_id)
    return goods(request, {'goods':filtered, 'brands':Brand.objects.all()})
  
def payment(request):
    pass