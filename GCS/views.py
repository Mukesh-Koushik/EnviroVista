from django.shortcuts import render, redirect, get_object_or_404
from Users.templates import *
from .models import *
import json
from Users.models import CustomUser
import sys
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sessions.models import Session
from django.utils.timezone import now
import logging
logger = logging.getLogger(__name__)


def gcshome(request):
    products = Product.objects.filter( stock__gt=0 )
    categories = Category.objects.filter(is_active=True)
    return render(request, "EV_GCS.html", {'products':products, 'categories':categories})

def gcscategory(request):
    products = Product.objects.filter( stock__gt=0 )
    categories = Category.objects.filter(is_active=True)
    return render(request, 'EV_GCS_Category_Page.html')

def gcssearch(request):
    categories = Category.objects.filter(is_active=True)
    if request.method=="POST":
        search=request.POST.get('search')
        try:
            search_results = Product.objects.filter( name__icontains= search)
            return render(request, 'EV_GCS_Category_Page.html', {'search_results':search_results, 'categories':categories})
        except:
            return render(request, 'EV_GCS_Category_Page.html')
        

def gcsfilter(request):
    pass

def remove_from_cart(request):
    if request.method == "POST":
        data = json.loads(request.body)
        product_id = str(data.get("product_id"))  # Ensure product_id is a string for session

        if request.user.is_authenticated:
            try:
                item = CartItem.objects.get(user=request.user, product_id=product_id)
                if item.quantity > 1:
                    item.quantity -= 1
                    item.save()
                else:
                    item.delete()  # Remove from DB if quantity becomes 0
            except CartItem.DoesNotExist:
                return JsonResponse({'error': 'Item not found'}, status=400)
        else:
            cart = request.session.get("cart", {})

            if product_id in cart:
                if cart[product_id] > 1:
                    cart[product_id] -= 1  # Reduce quantity by 1
                else:
                    del cart[product_id]  # Remove item if quantity becomes 0

                request.session["cart"] = cart  # Save the updated cart

        return JsonResponse({"success": True})

    return JsonResponse({"error": "Invalid request"}, status=400)


#@login_required

def add_to_cart(request):
    if request.method == "POST":
        data = json.loads(request.body)
        product_id = data.get('product_id')

        if request.user.is_authenticated:
            # Handle authenticated users
            item, created = CartItem.objects.get_or_create(
                user=request.user, product_id=product_id
            )
            item.quantity += 1
            item.save()
        else:
            # Handle unauthenticated users using session
            cart = request.session.get('cart', {})  # Ensure 'cart' is a dictionary
            print("Cart before adding:", cart)  # Debugging log

            if product_id in cart:
                cart[str(product_id)] = cart.get(str(product_id), 0) + 1  # Update quantity
            else:
                cart[str(product_id)] = 1
            request.session['cart'] = cart  # Save the updated cart in the session

            print("Updated cart:", cart)  # Debugging log

        return JsonResponse({'success': True})

    return JsonResponse({'error': 'Invalid request'}, status=400)


def reduce_quantity(request):
    if request.method == "POST":
        data = json.loads(request.body)
        item_id = str(data.get("item_id"))  # Convert to string since session keys are strings

        cart = request.session.get("cart", {})

        if item_id in cart:
            if cart[item_id]["quantity"] > 1:
                cart[item_id]["quantity"] -= 1
            else:
                del cart[item_id]  # Remove item if quantity reaches 0

            request.session["cart"] = cart  # Update session
            request.session.modified = True  # Ensure session updates
    
    

def remove_product(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            product_id = data.get('product_id')
            cart = request.session.get('cart', {})
            pass
    except:
        pass


def place_order(request):
    print("Request method:", request.method)  # Debugging
    print("Received POST request")  # Debugging
    
    user = request.user
    cart = request.session.get("cart", {})

    product_id = request.POST.get("product_id")  
    address = request.POST.get("address", "Default Address")
    payment_mode = request.POST.get("payment_mode", "COD")

    print("Product ID:", product_id)  
    print("Address:", address)  
    print("Payment Mode:", payment_mode)  

    if product_id:  
        # Ordering a single product from the product description page
        product = get_object_or_404(Product, id=product_id)

        # If the product is in the cart, use its quantity; otherwise, assume 1
        quantity = cart.get(product_id, {}).get("quantity", 1)

        Orders.objects.create(
            user_id=user,
            prod_id=product,
            quantity=quantity,  # Save quantity
            mode_of_payment=payment_mode,
            order_status="ordered"
        )

        # Remove the product from the cart (if it was there)

    else:
        print(cart)
        if not cart:
            return JsonResponse({"success": False, "message": "Cart is empty!"}, status=400)

        # Ordering all items in the cart
        for item_id, item in cart.items():
            product = get_object_or_404(Product, id=item_id)

            Orders.objects.create(
                user_id=user,
                prod_id=product,
                quantity=item["quantity"],  # Save quantity
                mode_of_payment=payment_mode,
                order_status="ordered"
            )

        

    # Update session cart
    request.session["cart"] = cart
    request.session.modified = True

    return render(request, "EV_GCS_OrderConfirmationPage.html")




def checkout(request):
    total_price = 0
    cart_data=[]

    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        cart = {str(item.product_id): item.quantity for item in cart_items}
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        for item in cart_items:
            product = item.product  # Fetch product details
            cart_data.append({
                "product_id": product.id,
                "product_name": product.name,
                "product_image": product.image.url if product.image else None,
                "quantity": item.quantity,
                "price_per_item": float(product.price),  # Ensure Decimal compatibility
                "total_price": float(item.quantity * product.price),
            })
        print("Total price: ", total_price)
    else:
        cart = request.session.get("cart", {})
        
        product_ids = cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        for product in products:
            total_price += product.price * cart[str(product.id)]

    return render(request, 'EV_GCS_CartOverViewPage.html', {"cart": cart_data, "total_price": total_price})

def cartpayment(request):
    #raise Exception("🛑 view_cart() is executing but not logging!") 
    users = request.user
    address = users.location
    total_price = 0
    cart_data=[]
    print("Cartpayment called")
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        cart = {str(item.product_id): item.quantity for item in cart_items}
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        for item in cart_items:
            product = item.product  # Fetch product details
            cart_data.append({
                "product_id": product.id,
                "product_name": product.name,
                "product_image": product.image.url if product.image else None,
                "quantity": item.quantity,
                "price_per_item": float(product.price),  # Ensure Decimal compatibility
                "total_price": float(item.quantity * product.price),
            })
        #print("Total price: ", total_price)
    else:
        cart = request.session.get("cart", {})
        
        product_ids = cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        for product in products:
            total_price += product.price * cart[str(product.id)]
        
    return render(request, 'EV_GCS_PaymentPage.html', {"cart": cart_data, "total_price": total_price, "address": address})

# def updateaddress(request):
#     if request.method == 'POST':
#         newadd = request.POST.get("new_address")

#         address = CustomUser(location = newadd)
#         address.save()
#         return redirect(cartpayment)
#     else:
#         return redirect(cartpayment)

def orderTracking(request, order_id):
    address = request.user.location
    uid = request.user.id
    try:
        order = Orders.objects.get(id = order_id, user_id = uid)
    except:
        return redirect(gcshome)
    context = {
        "order" : order,
        "tracking_status" : {
            "ordered": "green" if order.status in ["ordered", "shipped", "out_for_delivery", "delivered"] else "gray",
            "shipped": "green" if order.status in ["shipped", "out_for_delivery", "delivered"] else "gray",
            "out_for_delivery": "yellow" if order.status == "out_for_delivery" else "gray",
            "delivered": "gray" if order.status != "delivered" else "green",
        },
    }
    return render(request,"EV_GCS_OrderTracking.html", {"context": context, "address": address})

# def checkout(request):
#     total_price = 0

#     if request.user.is_authenticated:
#         cart = request.session.get("cart", {})
        
#         # Fetch product prices from the database
#         product_ids = cart.keys()
#         products = Product.objects.filter(id__in=product_ids)

#         for product in products:
#             total_price += product.price * cart[str(product.id)]
#             print(total_price)
#             print(cart[str(product.id)])
#             print(product.price)
#             print("----")

#     return render(request, 'EV_GCS_CartOverViewPage.html', {"cart": cart, "total_price": total_price})



# def save_cart(request):
#     if request.method == 'POST':
#         cart_data = json.loads(request.body).get('cart')
#         print("Recieved cart data")
#         request.session['cart'] = cart_data
#         print("Updated cart data")
#         return JsonResponse({'status': 'Cart updated successfully'})
#     return JsonResponse({'error': 'Invalid request'}, status=400)



#@login_required
def view_cart(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        cart = {item.product_id: item.quantity for item in cart_items}
        print("View_cart activated")
    else:
        cart = request.session.get('cart', {})

    return JsonResponse({'cart': cart})

# @login_required
# def remove_from_cart(request, item_id):
#     cart_item = get_object_or_404(CartItem, id=item_id)
#     cart_item.delete()
#     return redirect('cart_detail')



def gcscategorydescription(request):
    return render(request, "EV_GCS_Category_Description_Page.html")

def gcsorderconfirmation(request):
    return render(request, "EV_GCS_OrderConfirmationPage.html")



def gcsreturnpage(request):
    return render(request, "EV_ReturnAndRefundPage.html")

def gcsyourorders(request):
    return render(request, "EV_YourOrdersPage.html")
        
# def gcsfilter(request):
#     filter_type = request.GET.get('filter', 'all')
#     if filter_type == 'in-stock':
#         products = Product.objects.filter(stock__gt=0)
#     elif filter_type == 'out-of-stock':
#         products = Product.objects.filter(stock=0)
#     else:
#         products = Product.objects.all()

#     return render(request, 'gcs_homepage.html', {'products': products})

    

