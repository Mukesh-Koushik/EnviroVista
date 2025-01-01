from django.shortcuts import render, redirect, get_object_or_404
from Users.templates import *
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


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

def addtocart(request):
    
    pass


def gcscartoverview(request):
    return render(request, "EV_GCS_CartOverViewPage.html")

def gcscategorydescription(request):
    return render(request, "EV_GCS_Category_Description_Page.html")

def gcsorderconfirmation(request):
    return render(request, "EV_GCS_OrderConfirmationPage.html")

def gcspaymentpage(request):
    return render(request, "EV_GCS_PaymentPage.html")

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

    

