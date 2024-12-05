from django.shortcuts import render, redirect
from Users.templates import *


def login_signup(request):
    return render(request, 'Login_Signup.html')



# Create your views here.
