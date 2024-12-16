from django.shortcuts import render, redirect
from Users.templates import *
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def gcshome(request):
    return render(request, "EV_GCS.html")

