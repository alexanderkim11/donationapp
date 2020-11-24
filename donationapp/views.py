# /***************************************************************************************
# *  REFERENCES
# *  Title: Django - Form Processing
# *  Author: tutorialspoint
# *  Date: 10/10/20
# *  Code version: v1.0.0
# *  URL: https://www.tutorialspoint.com/django/django_form_processing.htm
# *  Software License: Fair Use
# *
# *  Title: Django Forms
# *  Author: Educba
# *  Date: 10/12/20
# *  Code version: v1.0.0
# *  URL: https://www.educba.com/django-forms/
# *  Software License: Fair Use
# *
# *  Title: Django Tutorial Part 9: Working with forms
# *  Author: MDN web docs
# *  Date: 10/16/20
# *  Code version: v1.0.0
# *  URL: https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Forms
# *  Software License: Fair Use
# *
# *  Title: Working with forms
# *  Author: django
# *  Date: 10/18/20
# *  Code version: 3.1.3
# *  URL: https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Forms
# *  Software License: BSD-3
# *
# *  Title: Django date query from newest to oldest
# *  Author: mipadi from stack overflow
# *  Date: 11/7/2020
# *  Code version: v1.0.0
# *  URL:https://stackoverflow.com/questions/30314741/django-date-query-from-newest-to-oldest
# *  Software License: Fair use
# *
# *  Title:  The Ultimate Guide to Django Redirects
# *  Author:  Daniel Hepper
# *  Date: 11/23/2020
# *  Code version: Python 3
# *  URL:https://realpython.com/django-redirects/
# *
# *  Title:Handling Multiple Forms on the Same Page in Django
# *  Author:Lakshmi Narasimhan
# *  Date: 11/11/2020
# *  Code version: v1.0.0
# *  URL:https://www.codementor.io/@lakshminp/handling-multiple-forms-on-the-same-page-in-django-fv89t2s3j
# *  Software License: All Rights Reserved
# *
# *  Title: django display message after POST form submit
# *  Authors: damio and Krishna Kumar Jangid from stackoverflow
# *  Date: 11/23/2020
# *  Code version: v1.0.0
# *  URL:https://stackoverflow.com/questions/28723266/django-display-message-after-post-form-submit
# *  Software License: Fair Use
# *
# ***************************************************************************************

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
from django.contrib import messages

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
                messages.success(request, 'Thank you for volunteering!')
            else:
                message = "You have already signed up for this opportunity"
                messages.warning(request, 'Form submission failed!')
    elif 'donate' in request.POST:
        if form1.is_valid():
            request.session['amount'] = request.POST['amount']
            request.session['cause'] = request.POST['cause']
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

@login_required
def checkout_confirmation(request):
    cause = Cause.objects.get(pk=request.session.get('cause'))
    transaction = Transaction()
    transaction.user = request.user
    transaction.date = datetime.datetime.now()
    transaction.amount = request.session.get('amount')
    transaction.cause = cause
    transaction.save()
    return render(request, 'donationapp/checkout_confirmation.html', {'amount' : request.session.get('amount'), 
        'cause' : cause})

def volunteer_opportunities(request):
    latest_volunteer_list = Volunteer_Opp.objects.order_by('date')
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
    form.instance.total_people = 0
    if form.is_valid():
        if form.instance.date != None:
            form.clean_date()
        form.save()
        return HttpResponseRedirect('/donationapp/volunteering')  # 4
    else:  # 5
        # Create an empty form instance
        form = VolunteerForm(request.POST or None)
    context = {'form': form}

    return render(request, 'donationapp/create_volunteer', context)


