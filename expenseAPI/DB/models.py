from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=20, unique=True, null=False)
    email = models.CharField(max_length=50, unique=True, null=False)
    password = models.CharField(max_length=20, null=False) # password is hashed while being stored in the database

    expenses = models.JSONField(default=list) # list of user's expenses

    token = models.CharField(max_length=50, null=False, unique=True) # a token that allows to perform operations on user's expenses list, hashed in the database

    created_at = models.DateField(auto_now_add=True)

class Expense(models.Model):
    title = models.CharField(max_length=50, null=False)
    amount = models.FloatField()
    category = models.CharField(max_length=50, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)