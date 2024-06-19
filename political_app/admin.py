from django.contrib import admin
from .models import Volunteer, Task, Client, Admin

# Register your models here.
admin.site.register(Volunteer)
admin.site.register(Task)
admin.site.register(Client)
admin.site.register(Admin)