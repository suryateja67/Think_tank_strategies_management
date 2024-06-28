# myapp/urls.py
from django.urls import path
from .views import Home, Login, ResetPassword, AdminCreate, VolunteerCreate, TaskCreate, ClientCreate, TaskList, ClientList, VolunteerList, ForgotPassword, TaskEdit, SingleVolunteer, SingleTask, SingleClient, AdminList, AdminEdit, VolunteerEdit, ClientEdit
urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('volunteer/', VolunteerCreate.as_view(), name='volunteer'),
    path('task/', TaskCreate.as_view(), name='task'),
    path('client/', ClientCreate.as_view(), name='client'),
    path('admin/', AdminCreate.as_view(), name='admin'),
    path('volunteer_list/', VolunteerList.as_view(), name='list_volunteer'),
    path('task_list/', TaskList.as_view(), name='list_task'),
    path('client_list/', ClientList.as_view(), name='list_client'),
    path('admin_list/', AdminList.as_view(), name='admin_list'),
    path('login/', Login.as_view(), name='login'),
    path('reset_password/', ResetPassword.as_view(), name='reset_password'),
    path('forgot_password/', ForgotPassword.as_view(), name='forgot_password'),
    path('task_edit/', TaskEdit.as_view(), name='task_edit'),
    path('single_volunteer/', SingleVolunteer.as_view(), name='single_volunteer'),
    path('single_task/', SingleTask.as_view(), name='single_task'),
    path('single_client/', SingleClient.as_view(), name='single_client'),
    path('admin_edit/', AdminEdit.as_view(), name='admin_edit'),
    path('volunteer_edit/', VolunteerEdit.as_view(), name='volunteer_edit'),
    path('client_edit/', ClientEdit.as_view(), name='client_edit'),
]
