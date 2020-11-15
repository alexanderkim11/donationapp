from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Cause, Transaction, Volunteer_Opp,Volunteer_Transaction
from .forms import TransactionForm, VolunteerSignUpForm
from django.urls import reverse
from .forms import TransactionForm, VolunteerForm
from django.conf import settings
from importlib import import_module
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import datetime

# Create your views here.
def index(request):
    form1 = TransactionForm(request.POST or None)
    form2 = VolunteerSignUpForm(request.POST or None)
    message = ''

    # if request.method == 'GET': # accessing website
    #if request.method == 'POST':  # submitting to form
    if 'volunteer' in request.POST:
        form2.instance.user = request.user
        all_transactions = Volunteer_Transaction.objects.all()
        new_request = True
        if form2.is_valid():
            model_instance = form2.save(commit=False)
            for transaction in all_transactions:
                if transaction.name == model_instance.name and transaction.user == model_instance.user:
                    new_request = False
            if new_request:
                form2.save()
            else:
                message = "You have already signed up for this opportunity"
    elif 'donate' in request.POST:
        form1.instance.user = request.user
        form1.instance.date = datetime.datetime.now()
        if form1.is_valid():
            request.session['amount'] = request.POST['amount']
            form1.save()
            return HttpResponseRedirect(reverse('donationapp:checkout'))

    # calculate total amount raised by the current user
    total_raised = 0
    if request.user.is_authenticated:
        all_transactions = Transaction.objects.filter(user=request.user)
        for transaction in all_transactions:
            total_raised = total_raised + transaction.amount

    context = {'form1': form1, 'form2': form2, 'nbar': 'home', 'total_raised': total_raised, 'message': message}
    return render(request, "donationapp/index.html", context)


@login_required
def account(request):
    # calculate total amount raised by the current user
    total_raised = 0
    all_transactions = Transaction.objects.filter(user = request.user)
    all_volunteer_transactions = Volunteer_Transaction.objects.filter(user = request.user)
    latest_volunteer_list= Volunteer_Opp.objects.order_by('date')

    volunteer_opps = []
    for opp in latest_volunteer_list:
        for transaction in all_volunteer_transactions:
            if str(transaction.name) == str(opp.name) and opp.date >=  datetime.date.today():
                volunteer_opps.append(opp)


    if request.method == 'GET':
        for transaction in all_transactions:
            total_raised = total_raised + transaction.amount
    level = total_raised // 100
    next_level = level + 1
    level_up = 100 - (total_raised % 100)

    context = {'nbar': 'account', 'all_transactions': all_transactions,'volunteer_opps':volunteer_opps, 'total_raised': total_raised, 'level' : level, 'next_level': next_level,'level_up': level_up}
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

@login_required
def checkout(request):
    return render(request, 'donationapp/checkout.html', {'amount' : request.session.get('amount')})

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

@login_required
def create_opportunity(request):
    form = VolunteerForm(request.POST or None)
    if form.is_valid():
        if form.instance.date != None:
            form.clean_date()
        form.save()
    context = {'form': form}

    return render(request, 'donationapp/create_volunteer', context)


