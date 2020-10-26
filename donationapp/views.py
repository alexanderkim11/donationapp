from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Cause, Transaction, Volunteer_Opportunity
from .forms import TransactionForm
from django.urls import reverse
from .forms import TransactionForm, VolunteerForm

# Create your views here.
def index(request):
    form = TransactionForm()

    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('donationapp:checkout', kwargs={'pk':form.cleaned_data['amount']}))

    context = {'form': form,'nbar': 'home'}
    return render(request, "donationapp/index.html", context)

def account(request):
    return render(request, "donationapp/account.html",{'nbar': 'account'})

def causes(request):
    latest_cause_list = Cause.objects.all()
    all_transactions = Transaction.objects.all()
    for cause in latest_cause_list:
        for transaction in all_transactions:
            if str(transaction.cause) == str(cause.name):
                cause.total_money = cause.total_money + transaction.amount
    context = {'latest_cause_list': latest_cause_list,'nbar': 'causes'}
    return render(request, 'donationapp/causes.html',context)

def checkout(request, pk):
    return render(request, 'donationapp/checkout.html', {'amount':pk})
    
def volunteer_opportunities(request):
    latest_volunteer_list = Volunteer_Opportunity.objects.all()
    context = {'latest_volunteer_list': latest_volunteer_list,'nbar': 'volunteer'}
    return render(request, 'donationapp/volunteer_opportunities.html',context)

def create_opportunity(request):
    form = VolunteerForm(request.POST or None)
    if form.is_valid():
        form.save()

    context = {'form': form}

    return render(request, 'donationapp/create_volunteer', context)
