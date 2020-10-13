from django.db import models

# Create your models here.
class Causes(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=512)
    total_money = models.FloatField()
    goal = models.FloatField()

    def __str__(self):
        return self.name
        
