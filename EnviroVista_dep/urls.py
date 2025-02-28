"""
URL configuration for EnviroVista_dep project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from Users.views import *
from Leaderboard.views import *
from GCS.views import *
from GCX.views import *
from Ecoaware.views import *
from django.contrib.auth.decorators import login_required
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_signup, name="loginpage"),
    path('logout/', my_logout, name='logout'),
    path('signup/', signup, name='signup'),
    path('logindb/', login, name='logindb'),
    path('', home, name='home'),
    path('gcshome/', gcshome, name='gcshome'),
    path('addtocart/', add_to_cart, name='addtocart'),
    path('viewcart/', view_cart, name='viewcart'),
    # path('save_cart/', save_cart, name='savecart'),
    path('gcscategory/', gcscategory, name='category'),
    path('gcscategorydesc/', gcscategorydescription, name='categorydesc'),
    path('gcsorderconfirm/', gcsorderconfirmation, name='orderconfirm'),
    #path('payment/', gcspaymentpage, name='payment'),
    path('returns/', gcsreturnpage, name='returnpage'),
    path('orders/', gcsyourorders, name='yourorders'),
    path('reduce_quantity/',  reduce_quantity, name='reducequantity'),
    path('place_order/', place_order, name='place_order'),
    path('ordertracking/', orderTracking, name='ordertracking'),
    #path('cartoverview/', gcscartoverview, name='cartoverview'),
    path('checkout/', checkout, name='checkout'),
    path('payment/', cartpayment, name='cartpayment1'),
    path('precheckout/', precheckout, name='cartpayment'),
    #path('updateaddress/', updateaddress, name='updateaddress'),
    path('ecoaware/', taskshome, name='ecoaware'),
    # path('ecoaware/submit/<int:task_id>/', ecoaware_display, name='ecoaware_display'),
    path('ecoaware/submit/<int:task_id>/', submit_task, name='submit_task'),
    path('ecoaware/upload_task/', upload_task, name='upload_task'),
    path('ideaforge/submit/', ideaforgeconf, name='ideaforgesub'),
    path('leaderboard/', leaderboard, name='leaderboard'),    
    path('upload/', submission, name='submission'),
    path('search/', gcssearch, name='searchdb'),
    path('ideaforge/', ideaforge, name='ideaforge'),
    path('profile/', login_required(profile), name='profile'),
    path('editprofile/', login_required(profileedit), name='editprofile'),


    #path('filter/<slug>:<slug>', gcsfilter, name="gcsfilter")
    #path('gcshome/', login_required(gcshome), name='gcshome'),
    #path('login/', auth_views.LoginView.as_view(template_name='Users/login.html'), name='login'),
    #path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

