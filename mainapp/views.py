from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from mainapp.models import Brand, Product
from userapp.forms import UserLoginForm
from userapp.models import User
from django.contrib import auth
from userapp.views import cart
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
            context = {'goods':Product.objects.all(),
                       'brands':Brand.objects.all(),
                       'form':UserLoginForm, 
                       'carts':cart(request), 
                       'range':range(len(cart(request)))}
        return render(request,'mainapp/goods.html', context)
    else:
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
        return HttpResponseRedirect('/')
        

def good(request):
    try:
        device_id = request.session['device_id']
    except KeyError:
        device_id = str(uuid.uuid4())
        request.session['device_id'] = device_id
    print(request.session['device_id'])
    
    good_id = request.GET.get('id')
    good_info = Product.objects.get(id=good_id)
    return render(request,'mainapp/good.html',{'good':good_info, 
                                               'brands':Brand.objects.all(), 
                                               'form':UserLoginForm, 
                                               'carts':cart(request)})

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