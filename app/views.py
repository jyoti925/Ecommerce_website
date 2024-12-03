from django.shortcuts import render,redirect
from django.views import View
from django.views.generic import ListView,DetailView
from .models import Customer, Product, Cart, OrderPlaced
from.forms import CustomerRegistrationForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse

# def home(request):
#  return render(request, 'app/home.html')

class ProductView(ListView):
 def get(self, request):
  topwears = Product.objects.filter(category='TW')
  bottomwears = Product.objects.filter(category='BW')
  mobile= Product.objects.filter(category='M')
  return render(request, 'app/home.html',{'topwears':topwears, 'bottomwears':bottomwears, 'mobile':mobile})

class ProductDetailView(DetailView):
 def get(self, request, pk):
    product = Product.objects.get(pk=pk)
    return render(request, 'app/productdetail.html',{'product':product})

def add_to_cart(request):
 user=request.user
 product_id = request.GET.get('prod_id')
 product=Product.objects.get(id=product_id)
 Cart(user=user, product=product).save()
 return redirect('/cart')

def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)  
        
        amount = 0.0
        shipping_amount = 70.0
        totalamount = 0.0

        if cart:
            for p in cart:
                tempamount = p.quantity * p.product.discounted_price
                amount += tempamount
            totalamount = amount + shipping_amount  

        return render(request, 'app/addtocart.html', {
            'carts': cart,
            'total_amount': totalamount,
            'amount': amount
        })
    else:
        # Optionally, you can return a redirect to login if the user is not authenticated
        return render(request, 'app/emptycart.html')

def buy_now(request):
 return render(request, 'app/buynow.html')

def profile(request):
 return render(request, 'app/profile.html')

def address(request):
 return render(request, 'app/address.html')

def orders(request):
 return render(request, 'app/orders.html')

def change_password(request):
 return render(request, 'app/changepassword.html')

def mobile(request, data=None):
 if data == None:
    mobiles= Product.objects.filter(category='M')
 elif data == 'Redmi' or  data=='Sumsung': 
   mobiles= Product.objects.filter(category='M').filter(brand=data)
   return render(request, 'app/mobile.html',{'mobiles':mobiles})

def login(request):
 return render(request, 'app/login.html')

class CustomerRegistrationView(View):
 def get(self, request):
  form= CustomerRegistrationForm()
  return render(request, 'app/customerregistration.html', {'form':form})
 def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulations!! Registered Successfully')
            form.save()
            # return render(request, 'success.html')
        return render(request, 'app/customerregistration.html', {'form': form})

def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']     
        c = Cart.objects.get(Q(product_id=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()

        amount = 0.0
        shipping_amount = 70.0
        cart_products = [p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_products:
            tempamount = p.quantity * p.product.discounted_price
            amount += tempamount
            
            data = {
                'quantity': c.quantity,
                'amount': amount,
                'totalamount': amount + shipping_amount,
            }

            return JsonResponse(data)
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']     
        c = Cart.objects.get(Q(product_id=prod_id) & Q(user=request.user))
        if c.quantity>1:
            c.quantity -= 1
            c.save()
        else:
           c.delete()

        amount = 0.0
        shipping_amount = 70.0
        cart_products = [p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_products:
            tempamount = p.quantity * p.product.discounted_price
            amount += tempamount
        
        data = {
            'quantity': c.quantity if c.quantity>0 else 0,
            'amount': amount,
            'totalamount': amount + shipping_amount,
        }

        return JsonResponse(data)
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')  # Safely get 'prod_id' from GET request
        try:
            # Fetch the cart item and delete it
            c = Cart.objects.get(Q(product_id=prod_id) & Q(user=request.user))
            c.delete()

            # Calculate the updated cart total
            amount = 0.0
            shipping_amount = 70.0
            cart_products = Cart.objects.filter(user=request.user)  # Only for the current user

            for p in cart_products:
                tempamount = p.quantity * p.product.discounted_price
                amount += tempamount

            # Prepare data for JSON response
            data = {
                'amount': amount,
                'totalamount': amount + shipping_amount,
            }

        except Cart.DoesNotExist:
            # Handle the case where the cart item does not exist
            data = {
                'error': "Item does not exist in the cart.",
            }
        
        return JsonResponse(data)

    return JsonResponse({'error': 'Invalid request method.'})

def checkout(request):
 user= request.user
 add= Customer.objects.filter(user=user)
 cart_items= Cart.objects.filter(user=user)
 amount=0.0
 shipping_amount= 70.0
 totalamount=0.0
 cart_products = [p for p in Cart.objects.all() if p.user==request.user]
 if cart_products:
    for p in cart_products:
        tempamount = p.quantity * p.product.discounted_price
        amount += tempamount
    totalamount=amount+shipping_amount
        
 return render(request, 'app/checkout.html',{'add':add, 'totalamount':totalamount})
