from django.shortcuts import render, redirect
from GCX.templates import *
from GCX.models import *

def GCXhome(request):
    return render(request, "EV_GCCExchange.html")


# Create your views here.
