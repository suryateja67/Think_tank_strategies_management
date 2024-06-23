# myapp/urls.py
from django.urls import path
from .views import Home, Login, ResetPassword, AdminCreate, VolunteerCreate, TaskCreate, ClientCreate, TaskList, ClientList, VolunteerList

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('volunteer/', VolunteerCreate.as_view(), name='volunteer'),
    path('task/', TaskCreate.as_view(), name='task'),
    path('client/', ClientCreate.as_view(), name='client'),
    path('volunteer_list/', VolunteerList.as_view(), name='list_volunteer'),
    path('task_list/', TaskList.as_view(), name='list_task'),
    path('client_list/', ClientList.as_view(), name='list_client'),
    path('admin/', AdminCreate.as_view(), name='admin'),
    path('login/', Login.as_view(), name='login'),
    path('reset_password/', ResetPassword.as_view(), name='reset_password')
]
