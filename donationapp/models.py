from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
# Create your models here.
class Cause(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=512)
    total_money = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.00)])
    goal = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.01)])

    def __str__(self):
        return self.name

class Transaction(models.Model):
    cause = models.ForeignKey(Cause, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.01)])
    date = models.DateTimeField('date published', null=True)

    def __str__(self):
        return "Cause: " + str(self.cause.name) + ", User: " + str(self.user.first_name) + ", Date: " + str(self.date)
        #return "Cause: " + str(self.cause.name) + ", User: " + str(self.user.first_name)

class Volunteer_Opp(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=512)
    date = models.DateField('date', null=True)
    begin = models.TimeField(auto_now=False, auto_now_add=False,null=True)
    end = models.TimeField(auto_now=False, auto_now_add=False,null=True)
    total_people = models.IntegerField(validators=[MinValueValidator(0)])
    people_needed = models.IntegerField( validators=[MinValueValidator(1)])

    def __str__(self):
        return self.name

class Volunteer_Transaction(models.Model):
    name = models.ForeignKey(Volunteer_Opp, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "Volunteer: " + str(self.name.name) + ", User: " + str(self.user.first_name)
