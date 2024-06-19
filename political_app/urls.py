# myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('volunteer', views.volunteer, name='volunteer'),
    path('task', views.task, name='task'),
    path('client', views.client, name='client'),
    path('volunteer_list', views.volunteer_list, name='list_volunteer'),
    path('task_list', views.task_list, name='list_task'),
    path('client_list', views.client_list, name='list_client'),
    path('admin', views.admin, name='admin'),
    path('login', views.login, name='login')
]
