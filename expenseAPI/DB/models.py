from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=20)
    email = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=20) # password is hashed while being stored in the database

    expenses = models.JSONField(default=list) # list of user's expenses

    token = models.CharField(max_length=50) # a token that allows to perform operations on user's expenses list, hashed in the database

    createdAt = models.DateField(auto_now_add=True)
