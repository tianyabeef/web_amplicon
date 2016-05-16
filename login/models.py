from django.db import models

# Create your models here.
from django.contrib import admin
# Create your models here.
class User(models.Model):
    userid = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
admin.site.register(User)
class FileUpload(models.Model):
    userid = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    file = models.CharField(max_length=50)


