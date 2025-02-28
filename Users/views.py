from django.shortcuts import render, redirect
from Users.templates import *
from .models import CustomUser
from GCS.models import *
from Ecoaware.models import *
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout



def login_signup(request):
    return render(request, 'Login_Signup.html')
 
def home(request):
    return render(request, "EV_Home.html")

def signup(request):
    if request.method=="POST":
        fname=request.POST.get('fname')
        lname=request.POST.get('lname')
        mail=request.POST.get('email')
        num=request.POST.get('num')
        password=request.POST.get('password')
        conf_pass=request.POST.get('conf_pass')

        if len(num)==10 and num.isdigit():
            pass
        else:
            messages.error(request, "Invalid mobile number!")
            return redirect('loginpage')
        
        if len(password)<8:
            messages.error(request, "Password should atleast contain 8 characters!")
            return redirect('loginpage')

        if password != conf_pass:
            messages.error(request, "Passwords do not match!")
            return redirect('loginpage')
        
        try:
            user = CustomUser.objects.create_user(username=mail,first_name=fname, last_name=lname, email=mail,password=password,phone_no=num,)
            user.save()
            messages.success(request, "Account created successfully!")
            return redirect('loginpage')
        except IntegrityError:
            messages.error(request, "Username already exists!")
            return redirect('loginpage')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, "Login successful!")
            return redirect('home')  
        else:
            messages.error(request, "Invalid username or password!")
            return redirect('loginpage')
        
def profile(request):
    user = request.user
    return render(request, 'EV_Profile.html', {"user": user})

def profileedit(request):
    if request.method == "POST":
        pass
    return render(request, 'EV_ProfileEdit.html')




def my_logout(request):
    logout(request)
    return redirect('home')
# Create your views here.

