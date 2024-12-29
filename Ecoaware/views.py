from django.shortcuts import render, redirect
from Ecoaware.templates import *
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def taskshome(request):
    grps=Tasks.objects.filter(mode="2")
    inds=Tasks.objects.filter(mode="1")
    return render(request, 'EV_EcoawareHomePage.html', {"grps":grps, "inds": inds})

def submission(request):
    return render(request, 'EV_TaskUploadPage.html')

def ideaforge(request):
    return render(request, 'EV_IdeaForge.html')
# Create your views here.
