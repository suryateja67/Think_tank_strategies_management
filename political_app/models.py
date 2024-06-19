from django.db import models

# Create your models here.
class Volunteer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True, default=None)
    password = models.CharField(max_length=100, default=None)
    roll = models.IntegerField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    role = models.CharField(max_length=100, default="volunteer")


class Admin(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True, default=None)
    password = models.CharField(max_length=100, default=None)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    role = models.CharField(max_length=100, default="admin")


class Task(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    roll = models.IntegerField(null=True, blank=True)
    volunteer = models.ForeignKey(Volunteer, on_delete=models.SET_NULL, default=None, null=True, blank=True)


class Client(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, default=None, null=True, blank=True)
    constituency = models.CharField(max_length=100, default=None, null=True, blank=True)
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    role = models.CharField(max_length=100, default="client")
    email = models.EmailField(max_length=100, unique=True, default=None)
    password = models.CharField(max_length=100, default=None)
    
