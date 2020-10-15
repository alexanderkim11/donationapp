from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Cause;
# Create your views here.
def index(request):
    return render(request, "donationapp/index.html",{'nbar': 'home'})

def account(request):
    return render(request, "donationapp/account.html",{'nbar': 'account'})

def causes(request):
    latest_cause_list = Cause.objects.all()
    context = {'latest_cause_list': latest_cause_list,'nbar': 'causes'}
    return render(request, 'donationapp/causes.html',context)
