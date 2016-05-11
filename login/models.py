from django.db import models

# Create your models here.
from django.contrib import admin
# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

admin.site.register(User)
