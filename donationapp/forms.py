from django import forms
from django.forms import ModelForm
from .models import Transaction

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