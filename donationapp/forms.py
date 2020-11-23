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
            fields = ["name", "description","date","begin","total_people", "people_needed"]
            model.total_people = 0
            widgets = {
                'name': forms.TextInput(attrs={'class': 'form-control'}),
                'description': forms.TextInput(attrs={'class': 'form-control'}),
                'date' : forms.DateInput(attrs={'class': 'form-control'}),
                'begin': forms.TimeInput(attrs={'class': 'form-control'}),
                'total_people': forms.TextInput(attrs={'class': 'form-control'}),
                'people_needed': forms.TextInput(attrs={'class': 'form-control'}),

            }
            labels = {
                'total_people' : 'People signed up',
                'people_needed' : 'Total People Needed',
                'date': 'Date'
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
