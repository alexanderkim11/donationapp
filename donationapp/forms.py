from django import forms
from django.forms import ModelForm
from .models import Transaction, Volunteer_Opportunity

class TransactionForm(ModelForm):
    class Meta:
            model = Transaction
            fields = ["amount", "cause", "user", "date"]

            widgets = {
                'amount': forms.TextInput(attrs={'class': 'form-control'}),
                'cause': forms.Select(attrs={'class': 'form-control'}),
                'user': forms.Select(attrs={'class': 'form-control'}),
                'date': forms.TextInput(attrs={'class': 'form-control'}),
            }

class VolunteerForm(ModelForm):
    class Meta:
            model = Volunteer_Opportunity
            fields = ["name", "description","total_people", "people_needed"]
            model.total_people = 0
            widgets = {

                'name': forms.TextInput(attrs={'class': 'form-control'}),
                'description': forms.TextInput(attrs={'class': 'form-control'}),
            }
            labels = {
                'total_people' : 'People signed up',
                'people_needed' : 'Total People Needed'
            }