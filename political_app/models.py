from django.db import models


class Volunteer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True, default=None)
    password = models.CharField(max_length=100, default=None)
    roll = models.IntegerField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=100, default="volunteer")


class Admin(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True, default=None)
    password = models.CharField(max_length=100, default=None)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=100, default="admin")


class Client(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, default=None, null=True, blank=True)
    constituency = models.CharField(max_length=100, default=None, null=True, blank=True)
    total_amount = models.IntegerField(null=True, blank=True, default=None)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    role = models.CharField(max_length=100, default="client")
    email = models.EmailField(max_length=100, unique=True, default=None)
    password = models.CharField(max_length=100, default=None)
    created_at = models.DateTimeField(auto_now_add=True)


class Task(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    roll = models.IntegerField(null=True, blank=True)
    volunteers = models.ManyToManyField(Volunteer, related_name='tasks', blank=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, default=None, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, default="pending")
    
