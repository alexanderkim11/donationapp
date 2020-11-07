from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Cause, Transaction, Volunteer_Opp,Volunteer_Transaction
from .forms import TransactionForm, VolunteerSignUpForm
from django.urls import reverse
from .forms import TransactionForm, VolunteerForm
from django.conf import settings
from importlib import import_module

# Create your views here.
def index(request):
    form = TransactionForm()

    # if request.method == 'GET': # accessing website
    if request.method == 'POST': # submitting to form
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('donationapp:checkout', kwargs={'pk':form.cleaned_data['amount']}))
        
    # calculate total amount raised by the current user
    total_raised = 0
    if request.method == 'GET':
        all_transactions = Transaction.objects.filter(user = request.user)
        for transaction in all_transactions:
            total_raised = total_raised + transaction.amount

    context = {'form': form,'nbar': 'home', 'total_raised': total_raised}
    return render(request, "donationapp/index.html", context)

def account(request):
    # calculate total amount raised by the current user
    total_raised = 0
    if request.method == 'GET':
        all_transactions = Transaction.objects.filter(user = request.user)
        for transaction in all_transactions:
            total_raised = total_raised + transaction.amount
    level = total_raised // 100

    context = {'nbar': 'account', 'total_raised': total_raised, 'level' : level}
    return render(request, "donationapp/account.html",context)



def causes(request):
    latest_cause_list = Cause.objects.all()
    all_transactions = Transaction.objects.all()

    # sum across all transactions to add total amount raised for cause
    for cause in latest_cause_list:
        total = 0
        for transaction in all_transactions:
            if str(transaction.cause) == str(cause.name):
                total = total + transaction.amount
        cause.total_money = total
        cause.save()
    context = {'latest_cause_list': latest_cause_list,'nbar': 'causes'}
    return render(request, 'donationapp/causes.html',context)

def checkout(request, pk):
    return render(request, 'donationapp/checkout.html', {'amount':pk})
    
def volunteer_opportunities(request):
    latest_volunteer_list = Volunteer_Opp.objects.all()
    all_transactions = Volunteer_Transaction.objects.all()
    for cause in latest_volunteer_list:
        total = 0
        for transaction in all_transactions:
            if str(transaction.name) == str(cause.name):
                total = total + 1
        cause.total_people = total
        cause.save()
    context = {'latest_volunteer_list': latest_volunteer_list,'nbar': 'volunteer'}
    return render(request, 'donationapp/volunteer_opportunities.html',context)

def create_opportunity(request):
    form = VolunteerForm(request.POST or None)
    if form.is_valid():
        form.save()

    context = {'form': form}

    return render(request, 'donationapp/create_volunteer', context)

def volunteer_signup(request):
    form = VolunteerSignUpForm(request.POST or None)
    if form.is_valid():
        form.save()

    context = {'form': form}

    return render(request, 'donationapp/volunteer_signup.html', context)
