from django.contrib import admin
from .models import Cause, Transaction, Volunteer_Opp,Volunteer_Transaction
# Register your models here.
admin.site.register(Cause)
admin.site.register(Transaction)
admin.site.register(Volunteer_Opp)
admin.site.register(Volunteer_Transaction)
