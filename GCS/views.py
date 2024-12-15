from django.shortcuts import render, redirect
from Users.templates import *
from .models import *
from django.contrib import messages


def home(request):
    return render(request, "EV_GCS.html")

