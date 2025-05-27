from django.db import models

from django.contrib.auth.models import User

# Create your models here.

class Account(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	balance = models.IntegerField()

class Card(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    number = models.CharField(max_length=16)
