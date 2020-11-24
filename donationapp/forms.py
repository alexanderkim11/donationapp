# /***************************************************************************************
# *  REFERENCES
# *  Title: Django: How to set DateField to only accept Today & Future dates
# *  Author: Arnaud from Stack overflow
# *  Date:  11/6/2020
# *  Code version: Version 1
# *  URL:https://stackoverflow.com/questions/4941974/django-how-to-set-datefield-to-only-accept-today-future-dates
# *  Software License: Fair use
# *
# *  Title: how can I change the modelform label and give it a custom name
# *  Author: solarissmoke from stackoverflow
# *  Date:  10/20/2020
# *  Code version: v1.0.0
# *  URL:https://stackoverflow.com/questions/36905060/how-can-i-change-the-modelform-label-and-give-it-a-custom-name
# *  Software License: Fair Use
# *
# *  Title: Forms
# *  Author: Bootstrap
# *  Date: 10/11/2020
# *  Code version: Bootstrap 4
# *  URL:https://getbootstrap.com/docs/4.0/components/jumbotron/
# *  Software License:  MIT license
# *
# ***************************************************************************************



from django import forms
from django.forms import ModelForm
from .models import Transaction, Volunteer_Opp, Volunteer_Transaction
import datetime

class TransactionForm(ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'
    class Meta:
            model = Transaction
            fields = ["amount", "cause"]

            widgets = {
                'amount': forms.TextInput(attrs={'class': 'form-control'}),
                'cause': forms.Select(attrs={'class': 'form-control'}),
            }

class VolunteerForm(ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'
    class Meta:
            model = Volunteer_Opp
            fields = ["name", "organization","description","date","begin", "people_needed"]
            model.total_people = 0
            widgets = {
                'name': forms.TextInput(attrs={'class': 'form-control'}),
                'organization': forms.TextInput(attrs={'class': 'form-control'}),
                'description': forms.TextInput(attrs={'class': 'form-control'}),
                'date': forms.DateInput(attrs={'class': 'form-control','type':'date'}),
                'begin': forms.TimeInput(attrs={'class': 'form-control','type':'time'}),
                'people_needed': forms.TextInput(attrs={'class': 'form-control'}),

            }
            labels = {
                'people_needed' : 'Total People Needed',
                'date': 'Date',
                'name':'Event'
            }

    def clean_date(self):
        date = self.cleaned_data['date']
        if date < datetime.date.today():
            raise forms.ValidationError("The date cannot be in the past!")
        return date

class VolunteerSignUpForm(ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'
    class Meta:
            model = Volunteer_Transaction
            fields = ["name"]
            widgets = {
                'name': forms.Select(attrs={'class': 'form-control'}),
            }
