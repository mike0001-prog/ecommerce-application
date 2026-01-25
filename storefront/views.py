from django.contrib.auth.decorators import login_required
from .models import Product,Order,OrderItem,WishList,WishListItem,Category
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .cart import CartManager
from authentication.forms import ShippingInfoForm
from authentication.models import ShippingInfo,AnonymousUserShippingInfo
from django.contrib  import messages
from .models import Order
from django.db.models import Q
from django.db.models.functions import Lower
from allauth.account.views import LogoutView
from  django.conf import settings
import requests
from .utils import create_order



def home(request):
    print(request.user)
    products = Product.objects.all()
    category = Category.objects.all()
    if request.user.is_authenticated:
        wishlist = WishList.objects.get(user=request.user)
        wishlistitem = WishListItem.objects.filter(wishlist=wishlist)
        ids = {f"{w.product.id}":w.product.id for w in wishlistitem}
        # print(ids)
        
        context = {"title":"Home","products":products,"wishlistitemids":ids,"category":category}
    else:
        context = {"title":"Home","products":products,"category":category}        
    # products = ['product1','product2','product3','product4','product5']

    # if request.method == 'POST':
    #     searched = request.POST['search']
    #     product = Product.objects.filter(name=searched)
    #     print(product)
    #     if product.exists():
    #         print(product.id)
    #         return redirect("product_info"/confirmed_product.name)
   
    return render(request,"storefront/store_home.html",context)

def product_details(request,name):
    cart = CartManager(request)
    product = Product.objects.get(name=name)
    cart.recentlys_viewed(name=product.name)
    category = product.cat
    product_in_the_same_cat = Product.objects.filter(cat=category)
    cart = CartManager(request)
    quantities = cart.get_quants()
    if request.user.is_authenticated:
        wishlist = WishList.objects.get(user=request.user)
        wishlistitem = WishListItem.objects.filter(wishlist=wishlist,product=product)
        context = {"product": product,
                "products":product_in_the_same_cat,
                "quants":quantities,
                "wishlistitem":wishlistitem}
    else:
        context = {"product": product,
                "products":product_in_the_same_cat,
                "quants":quantities}
    return render(request,"storefront/product_details.html",context)
def add(request):
    cart = CartManager(request)
    
    if request.method == "POST":
        print(request.POST)
        product_id = int(request.POST.get("product_id"))
        product_qty = int(request.POST.get("product_qty"))
        # print(product_id)
        # print(product_qty)
        product = get_object_or_404(Product,id=product_id)
        cart.add(product=product,quantity=product_qty)
        qty = cart.__len__()
        total  = cart.calculate_total()
        print(total)
        return JsonResponse({"msg":"product added","qty":qty,"total":total})

def cart_summary(request):
    cart = CartManager(request)
    products = cart.get_products()
    quantities = cart.get_quants()
    total = cart.calculate_total()
    recent = cart.return_recently_viewed()
    
    context={"products":products,"quantities":quantities,"total":total,"recent":recent}
    return render(request,"storefront/cart.html",context)


def cart_remove(request):
    cart = CartManager(request)
    total = cart.calculate_total()
    quantities = cart.get_quants()
    new_total = 0
    if request.method == "POST":
        product_id_string = str(request.POST.get("product_id"))
        product_id = int(request.POST.get("product_id"))
        # print(product_id)
        # print(product_qty)
        product = get_object_or_404(Product,id=product_id)
        if product_id_string in quantities:
            product_price = quantities[product_id_string] * product.price
            new_total = total - product_price
        cart.cart_remove(product=product)
        qty = cart.__len__()
        return JsonResponse({"msg":"product removed ","total":new_total,"qty":qty})
def checkout(request):
    cart = CartManager(request)
    products = cart.get_products()
    quantities = cart.get_quants()
    total = cart.calculate_total()
    form = ShippingInfoForm()
    if request.method == "POST":
       
        if request.user.is_authenticated:
            form = ShippingInfoForm(request.POST,instance=request.user.shippinginfo)
            phone = request.POST["recipient_phone"]
            lg_area = request.POST["lg_area"]
            address = request.POST["recipient_address"]
            compounded_address = f"{address}\n at {lg_area} Local Government Area"
            my_order_info = {"phone":phone,"address":compounded_address}
            request.session["order_info"] = my_order_info
            print(request.session.get("order_info"))
        else:
            # print(request.POST)
            form = ShippingInfoForm(request.POST)
            # print(request.user)
            phone = request.POST["recipient_phone"]
            lg_area = request.POST["lg_area"]
            address = request.POST["recipient_address"]
            name = request.POST["recipient_name"]
            print(form.is_valid())
            if form.is_valid():
                AnonymousUserShippingInfo.objects.create(recipient_phone=phone,lg_area=lg_area,recipient_address=address,recipient_name=name)
                compounded_address = f"{address}\n at {lg_area} Local Government Area"
                my_order_info = {"phone":phone,"address":compounded_address}
                request.session["order_info"] = my_order_info
                return redirect('storefront_billing')
            else:
                messages.error(request, "Invalid Input")
        if form.is_valid():
            form.save()
            return redirect('storefront_billing')
    else:
        if request.user.is_authenticated:
            form = ShippingInfoForm(instance=request.user.shippinginfo)
        
    context = {"form":form,"products":products,"quantities":quantities,"total":total}
    return render(request,"storefront/checkout.html",context)
def billing(request):
    cart = CartManager(request)
    products = cart.get_products()
    quantities = cart.get_quants()
    total = cart.calculate_total()
    order_info = request.session.get("order_info")

    if request.method == "POST":
        print(request.POST)
        # print(request.POST["mode"].lower())
        if request.POST["mode"].lower() == "epayment":
            order = Order.objects.create(user=request.user or None,
                                phone=order_info["phone"],
                                shipping_address=order_info["address"],
                                amount_paid=total,
                                mode=request.POST["mode"])
        
            order_id = order.pk
            for product in products:
                for key,value in quantities.items():
                    id = int(key)
                    if id == product.id:
                        p = Product.objects.get(id = product.id)
                        OrderItem.objects.create(order=order,
                                                product=p,
                                                user=request.user,
                                                quantity = value,
                                                price=product.price)
            
            return redirect("payment_page")
        else:
            create_order(user=request.user,
                        phone=order_info["phone"],
                        addr=order_info["address"],
                        total=total,
                        mode=request.POST["mode"],
                        request=request)
           
            cart = CartManager(request)
            cart.checkout()

            return redirect('success_page')

    context = {"products":products,"quantities":quantities,"total":total,"title":"Billing"}
    return render(request,"storefront/billing.html",context)

def orders(request):
    # orders = Order.objects.filter(shipped=True)
    # no_of_shipped = len(Order.objects.filter(shipped=True))
    # no_of_pending = len(Order.objects.filter(shipped=False))
    orders = Order.objects.all()
    condition =True
    if request.method == "POST":
        condition = False
        orders = Order.objects.filter(shipped=False)
        return redirect("storefront_orders")
    context = {"orders":orders,
               "condition":condition}
    return render(request,"storefront/orders.html",context)

def like(request):
    if request.method == "POST":
        product_id = request.POST["product_id"]
        product = Product.objects.get(id=product_id)
        wishlist = WishList.objects.get(user = request.user)
        wishlistitem = WishListItem.objects.filter(wishlist=wishlist,product = product)
        print(request.POST)
        length = len(wishlistitem)
        if request.POST["action"]  == "like":
            WishListItem.objects.create(wishlist=wishlist,product=product)
            print("add like")
            return JsonResponse({"msg":f"{product.name} added to wish list","action":"like" })
        elif request.POST["action"] == "unlike":
            WishListItem.objects.get(wishlist=wishlist,product=product).delete()
            return JsonResponse({"msg":f"{product.name} removed to wish list","action":"unlike" })
        # try:
        #     wishlistitem = WishListItem.objects.filter(product = product,wishlist=wishlist)
        #     print(wishlistitem)
        #     return JsonResponse({"msg":f"{product.name} already added to wish list" })
        # except Exception:
        #     WishListItem.objects.create(wishlist=wishlist,product=product)
        #     return JsonResponse({"msg":"product added to wish list"})
    return JsonResponse({"msg":"bad request"})
@login_required
def wishlist(request):
    wishlist = WishList.objects.get(user=request.user)
    wishlistitems = WishListItem.objects.filter(wishlist=wishlist)
    context = {"wishlistitems":wishlistitems}
    return render(request,"storefront/wishlist.html",context)

# def settings(request):
#     pass

def search(request):
    if request.method == "POST":
        search_query = request.POST["search"]
        formatted = search_query.lower()
        if request.POST["action"] == "oninput":
            products = Product.objects.filter(Q(name__istartswith=formatted) | 
                                              Q(name__icontains=formatted))
            print(products)
            products_dict = {"product":{"id":p.id,"name":p.name} for p in products[:5] }
            return JsonResponse(products_dict)
        elif request.POST["action"] == "submit":
            products = Product.objects.filter(
                Q(name__icontains=formatted)| 
                Q(cat__name__icontains=formatted)).order_by(Lower("name"))
            context = {"products":products}
            if request.user.is_authenticated:
                wishlist = WishList.objects.get(user=request.user)
                wishlistitem = WishListItem.objects.filter(wishlist=wishlist)
                ids = {f"{w.product.id}":w.product.id for w in wishlistitem}
        # print(ids)
        
                context = {"title":"Search Products","products":products,"wishlistitemids":ids}
            return render(request,"storefront/search.html",context)
    else:
        return JsonResponse({"msg":"bad request"})

def payment_page(request):
    return render(request,"storefront/payment_page.html")
    
def sucess_page(request):
    return render(request,"storefront/success_page.html")

def verify_payment(request):
    reference = request.GET.get("reference")

    url = f"https://api.paystack.co/transaction/verify/{reference}"

    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_PUBLIC_KEY}",
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    if data["status"] and data["data"]["status"] == "success":
        return JsonResponse({
            "message": "Payment successful!",
            "amount": data["data"]["amount"],
            "reference": reference
        })

    return JsonResponse({"message": "Payment verification failed"})

def failure_page(request):
    context = {"info": "payment failed"}
    return render(request,"storefront/failure_page.html" ,context)

def category(request,name):
    products = Product.objects.filter(cat=Category.objects.get(name=name))
    if request.user.is_authenticated:
        wishlist = WishList.objects.get(user=request.user)
        wishlistitem = WishListItem.objects.filter(wishlist=wishlist)
        ids = {f"{w.product.id}":w.product.id for w in wishlistitem}
        context = {"products":products,}
        context = {"title":"Home","products":products,"wishlistitemids":ids,"name":name}
    context = {"products":products,"name":name}
    return render(request,"storefront/categories.html",context)