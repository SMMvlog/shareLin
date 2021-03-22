from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.views import View
from django.db.models import Q
from .models import *
from .forms import *


class Home(View):
    def get(self,request):
        mobile = Product.objects.filter(category = "M")
        laptop = Product.objects.filter(category = "L")
        laptop = Product.objects.filter(category = "L")
        topwears = Product.objects.filter(category = "TW")
        bottomwears = Product.objects.filter(category ="BW")
        return render(request, 'app/home.html',{'mobile':mobile,'laptop':laptop,'topwears':topwears,"bottomwears":bottomwears})


class product_detail(View):
    def get(self,request,pk):
        product = Product.objects.get(id=pk)
        already = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        return render(request, 'app/productdetail.html',{'product':product,'already':already})

def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    print(product)
    Cart(user=user,product=product).save()
    return redirect('/cart')

def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shiping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        if cart_product:
            for p in cart_product:
                temp = (p.quantity) * (p.product.discounted_price)
                amount += temp
                total_amount = amount + shiping_amount
            return render(request, 'app/addtocart.html',{'cart':cart,'amount':amount,'total_amount':total_amount})
        return render(request, 'app/empty.html')

def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+= 1
        c.save()
        amount = 0.0
        shiping_amount = 70.0
        # total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        if cart_product:
            for p in cart_product:
                temp = (p.quantity) * (p.product.discounted_price)
                amount += temp
                total_amount = amount + shiping_amount
            data = {
                'quantity': c.quantity,
                'amount': amount,
                'total_amount': total_amount
            }
            return JsonResponse(data)
    
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-= 1
        c.save()
        amount = 0.0
        shiping_amount = 70.0
        # total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        if cart_product:
            for p in cart_product:
                temp = (p.quantity) * (p.product.discounted_price)
                amount += temp
                total_amount = amount + shiping_amount
            data = {
                'quantity': c.quantity,
                'amount': amount,
                'total_amount': total_amount
            }
            return JsonResponse(data)
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shiping_amount = 70.0
        # total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        if cart_product:
            for p in cart_product:
                temp = (p.quantity) * (p.product.discounted_price)
                amount += temp
                total_amount = amount + shiping_amount
            data = {
                'amount': amount,
                'total_amount': total_amount
            }
            return JsonResponse(data)

def buy_now(request):
 return render(request, 'app/buynow.html')

def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html',{'add':add,'Active':'btn-primary'})

def orders(request):
    order_placed = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html',{'order_placed':order_placed})

def mobile(request,data=None):
    if data == None:
        mobiles = Product.objects.filter(category = "M")
    elif data == 'Realme' or data == 'apple' or data == 'Blackberry':
        mobiles = Product.objects.filter(category = "M").filter(brand = data)
    elif data == 'below':
        mobiles = Product.objects.filter(category = "M").filter(discounted_price__lt = 20000)
    elif data == 'above':
        mobiles = Product.objects.filter(category = "M").filter(discounted_price__gt = 20000)
    return render(request, 'app/mobile.html',{'mobiles':mobiles})

def login(request):
 return render(request, 'app/login.html')

class Customerregistration(View):
    error = ""
    def get(self,request):
        forms = CustomUserCreationForm()
        return render(request, 'app/customerregistration.html',{'forms':forms})
    
    def post(self,request):
        forms = CustomUserCreationForm(request.POST)
        try:
           if forms.is_valid():
              forms.save()
              error = "No"
           else:
               error = "yes"
        except Exception:
            error = "yes"
        return render(request, 'app/customerregistration.html',{'forms':forms,"error":error})

    

def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shiping_amount = 70.0
    total_amount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == user]
    if cart_product:
        for p in cart_product:
            temp = (p.quantity) * (p.product.discounted_price)
            amount += temp
        total_amount = amount + shiping_amount
    return render(request, 'app/checkout.html',{'add':add,'totalamount':total_amount,'cart_items':cart_items})

class ProfileView(View):
    def get(self,request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html',{'form':form,'Active':'btn-primary'})

    def post(self,request):
        error = ""
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=user, name=name,locality=locality,city=city,state=state,zipcode=zipcode)
            reg.save()
            error = "No"
        else:
            error = "yes"
        return render(request, 'app/profile.html',{'form':form,'Active':'btn-primary','error':error})

def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity).save()
        c.delete()
    return redirect("orders")