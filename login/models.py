from django.db import models

# Create your models here.
from django.contrib import admin
# Create your models here.
class User(models.Model):
    userid = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

class FileUpload(models.Model):
    title = models.CharField(max_length=50)
    userid = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    file = models.CharField(max_length=50)
    def __str__(self):
        return self.title
admin.site.register(User)

