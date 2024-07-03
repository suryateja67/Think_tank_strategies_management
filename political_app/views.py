import string, secrets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from political_app.models import Volunteer, Task, Client, Admin
from .utils import hash_password, check_password, check_unique_email, generate_jwt, admin_access, volunteer_access, client_access
from django.shortcuts import render


class Home(APIView): 
    def get(self, request):
        if request.data.get('role') in ['admin', 'volunteer']:
            return Response("Welcome to the application")
        return Response ('Unauthorized', status=status.HTTP_401_UNAUTHORIZED)


class Login(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response({'error': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            admin = Admin.objects.get(email=username)
            if check_password(admin.password, password):
                return Response({'message': 'Login successful',
                                 'admin': admin.name,
                                 'token': generate_jwt(admin.role, admin.id)}, status=status.HTTP_200_OK)
        except Admin.DoesNotExist:
            try:
                volunteer = Volunteer.objects.get(email=username)
                if check_password(volunteer.password, password):
                    return Response({'message': 'Login successful',
                                     'volunteer': volunteer.name,
                                     'token': generate_jwt(volunteer.role, volunteer.id)}, status=status.HTTP_200_OK)
            except Volunteer.DoesNotExist:
                return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)


class ResetPassword(APIView):
    def post(self, request):
        user_name = request.data.get('user_name')
        password = request.data.get('password')
        new_password = request.data.get('new_password')
        if user_name and password and new_password:
            try:
                admin = Admin.objects.get(email=user_name)
                if check_password(admin.password, password):
                    admin.password = hash_password(new_password)
                    admin.save()
                    return JsonResponse({'message': 'Password reset successful'}, status = 200)
            except Admin.DoesNotExist:
                try:
                    volunteer = Volunteer.objects.get(email=user_name)
                    if check_password(volunteer.password, password):
                        volunteer.password = hash_password(new_password)
                        volunteer.save()
                        return JsonResponse({'message': 'Password reset successful'}, status = 200)
                except Volunteer.DoesNotExist:
                    pass
            return JsonResponse({'error': 'Invalid credentials.'}, status=401)
        else:
            return JsonResponse({'error': 'Username, password and new password are required.'}, status=400)
        

class ForgotPassword(APIView):
    def post(self, request):
        user_name = request.data.get('user_name')
        if user_name:
            try:
                admin = Admin.objects.get(email=user_name)
                if admin:
                    password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(12))
                    admin.password = hash_password(password)
                    admin.save()
                    subject = 'New password alert'
                    message = f'''Hello {admin.name},

    Your new password is {password}
    Please reset your password as soon as possible.

    Best regards,
    Think Tank Strategies'''
                    send_mail(
                        subject,
                        message,
                        settings.EMAIL_HOST_USER,
                        [admin.email],
                        fail_silently=False,
                    )
                    return JsonResponse({'message': 'New password sent'}, status = 200)
            except Admin.DoesNotExist:
                try:
                    volunteer = Volunteer.objects.get(email=user_name)
                    if volunteer:
                        password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(12))
                        volunteer.password = hash_password(password)
                        volunteer.save()
                        subject = 'New password alert'
                        message = f'''Hello {admin.name},

    Your new password is {password}
    Please reset your password as soon as possible.

    Best regards,
    Think Tank Strategies'''
                    send_mail(
                        subject,
                        message,
                        settings.EMAIL_HOST_USER,
                        [admin.email],
                        fail_silently=False,
                    )
                    return JsonResponse({'message': 'New password sent'}, status = 200)
                except Volunteer.DoesNotExist:
                    return JsonResponse({'error': 'User does not exist'}, status=404)
        else:
            return JsonResponse({'error': 'Username is required.'}, status=400)
        

class AdminCreate(APIView):
    def post(self, request):
        if admin_access(request.data.get('token')):
            name = request.data.get('name')
            phone_number = request.data.get('phone_number')
            email = request.data.get('email')
            alphabet = string.ascii_letters + string.digits
            password = ''.join(secrets.choice(alphabet) for _ in range(12))
            
            if name and email and password:
                if check_unique_email(email):
                    admin = Admin.objects.create(name=name, phone_number=phone_number, email=email, password=hash_password(password))
                    if admin:
                        subject = 'Admin Account Created'
                        message = f'''Hello {name},

    Your account has been created with user_name {email} and password is {password}
    Please reset your password as soon as possible.

    Best regards,
    Think Tank Strategies'''

                        send_mail(
                            subject,
                            message,
                            settings.EMAIL_HOST_USER,
                            [admin.email],
                            fail_silently=False,
                        )
                        return JsonResponse({'message': f'Admin created with name: {name}'}, status=200)
                    else:
                        return JsonResponse({'message': 'Some error occurred'}, status=400)
                else:
                    return JsonResponse({'message': 'Email already exists'}, status=400)
            else:
                return JsonResponse({'message': 'Name and email must be provided'}, status=400)
        else:  
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)


class VolunteerCreate(APIView):
    def post(self, request):
        if admin_access(request.data.get('token')):
            name = request.data.get('name')
            roll = request.data.get('roll')
            phone_number = request.data.get('phone_number')
            email = request.data.get('email')
            alphabet = string.ascii_letters + string.digits
            password = ''.join(secrets.choice(alphabet) for _ in range(12))
            
            if name and email and password:
                if check_unique_email(email):
                    volunteer = Volunteer.objects.create(name=name, roll=roll, phone_number=phone_number, email=email, password = hash_password(password))

                    if volunteer:
                        subject = 'Volunteer Account Created'
                        message = message = f'''Hello {name},

        Your account has been created with user_name {email} and password is  {password}
        Please reset your password as soon as possible.

        Best regards,
        Think Tank Strategies'''
                        send_mail(
                            subject,
                            message,
                            settings.EMAIL_HOST_USER,
                            [volunteer.email],
                            fail_silently=False,
                        )
                    return JsonResponse({'message': f'Volunteer created with name : {volunteer.name}'})
                else:
                    return JsonResponse({'message': 'Email already exists'}, status=400)
            else:
                return JsonResponse({'error': 'Name and roll parameters are required.'}, status=400)
        else:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)


class TaskCreate(APIView):
    def post(self, request):
        if admin_access(request.data.get('token')):

            name = request.data.get('name')
            roll = request.data.get('roll')
            volunteer_id = request.data.get('volunteer_id')
            client_id = request.data.get('client_id')

            if not name or not roll:
                return Response({'error': 'Name and roll parameters are required.'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                task = Task.objects.create(name=name, roll=roll)

                if client_id:
                    try:
                        client = Client.objects.get(id=client_id)
                        task.client = client
                    except Client.DoesNotExist:
                        return Response({'error': 'Client not found.'}, status=status.HTTP_404_NOT_FOUND)

                if volunteer_id:
                    try:
                        volunteer = Volunteer.objects.get(id=volunteer_id)
                        task.volunteers.set([volunteer])
                    except Volunteer.DoesNotExist:
                        return Response({'error': 'Volunteer not found.'}, status=status.HTTP_404_NOT_FOUND)

                task.save()
                return Response({'message': f'Task created: {task.name}'}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)


class ClientCreate(APIView):
    def post(self, request):
        if admin_access(request.data.get('token')):
            name = request.data.get('name')
            phone_number = request.data.get('phone_number')
            constituency = request.data.get('constituency')
            task_id = request.data.get('task_id')
            image = request.FILES.get('image')
            email = request.data.get('email')
            alphabet = string.ascii_letters + string.digits
            password = ''.join(secrets.choice(alphabet) for _ in range(12))

            if not all([name, phone_number]):
                return Response({'error': 'Name, phone number parameters are required.'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                if task_id:
                    task_instance = Task.objects.get(id=task_id)
                else:
                    task_instance = None
            except Task.DoesNotExist:
                task_instance = None
            if check_unique_email(email):
                client = Client.objects.create(
                    name=name,
                    phone_number=phone_number,
                    constituency=constituency,
                    image=image,
                    task=task_instance,
                    email=email,
                    password= hash_password(password)
                )

                if client:
                    subject = 'Client Account Created'
                    message = f'''Hello {name},

            Your account has been created with user_name {email} and password is  {password}
            Please reset your password as soon as possible.

            Best regards,
            Think Tank Strategies'''
                    send_mail(
                        subject,
                        message,
                        settings.EMAIL_HOST_USER,
                        [client.email],
                        fail_silently=False,
                    )
                return Response({'message': f'Client created: {client.name}'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)


class VolunteerList(APIView):
    def get(self, request):
        if admin_access(request.data.get('token')):
            volunteers_instances = Volunteer.objects.all()
            volunteers = [
                {
                    'id': volunteer.id,
                    'name': volunteer.name,
                    'roll': volunteer.roll,
                    'tasks_counts': volunteer.tasks.count()
                }
                for volunteer in volunteers_instances
            ]
            return Response(volunteers, status=status.HTTP_200_OK) 
        else:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)


class TaskList(APIView):
    def get(self, request):
        if volunteer_access(request.data.get('token')):
            tasks_instances = Task.objects.all()
            tasks = [
                {
                    'id': task.id,
                    'name': task.name,
                    'roll': task.roll
                }
                for task in tasks_instances
            ]
            return Response(tasks, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

class AdminList(APIView):
    def get(self, request):
        print(admin_access(request.data.get('token')))
        if admin_access(request.data.get('token')):
            admins_instances = Admin.objects.all()
            admins = [
                {
                    'id': admin.id,
                    'name': admin.name,
                    'phone_number': admin.phone_number,
                    'email': admin.email
                }
                for admin in admins_instances
            ]
            return Response(admins, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)


class ClientList(APIView):
    def get(self, request):
        if admin_access(request.data.get('token')):
            clients_instances = Client.objects.all()
            clients = [
                {
                    'id': client.id,
                    'name': client.name,
                    'phone_number': client.phone_number,
                    'constituency': client.constituency,
                    'image': client.image.url if client.image else None
                }
                for client in clients_instances
            ]
            return Response(clients, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
class AdminEdit(APIView):
    def put(self, request):
        if admin_access(request.data.get('token')):
            id = request.data.get('id')
            name = request.data.get('name')
            phone_number = request.data.get('phone_number')
            email = request.data.get('email')
            amount_paid = request.data.get('amount_paid')
            if id:
                try:
                    admin = Admin.objects.get(id=id)
                    admin.name = name
                    admin.phone_number = phone_number
                    admin.email = email
                    admin.amount_paid = amount_paid
                    admin.save()
                    return Response({'message': 'Admin updated successfully'}, status=status.HTTP_200_OK)
                except Admin.DoesNotExist:
                    return Response({'error': 'Admin not found'}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({'error': 'ID required'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)


class ClientEdit(APIView):
    def put(self, request):
        if admin_access(request.data.get('token')):
            id = request.data.get('id')
            name = request.data.get('name')
            phone_number = request.data.get('phone_number')
            constituency = request.data.get('constituency')
            image = request.FILES.get('image')
            email = request.data.get('email')
            add_amount = request.data.get('add_amount')
            if id:
                try:
                    client = Client.objects.get(id=id)
                    client.name = name
                    client.phone_number = phone_number
                    client.constituency = constituency
                    client.image = image
                    client.email = email
                    client.total_amount += add_amount
                    client.save()
                    return Response({'message': 'Client updated successfully'}, status=status.HTTP_200_OK)
                except Client.DoesNotExist:
                    return Response({'error': 'Client not found'}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({'error': 'ID required'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        

class VolunteerEdit(APIView):
    def put(self, request):
        if admin_access(request.data.get('token')):
            id = request.data.get('id')
            name = request.data.get('name')
            roll = request.data.get('roll')
            email = request.data.get('email')
            phone_number = request.data.get('phone_number')
            if id:
                try:
                    volunteer = Volunteer.objects.get(id=id)
                    volunteer.name = name
                    volunteer.roll = roll
                    volunteer.email = email
                    volunteer.phone_number = phone_number
                    volunteer.save()
                    return Response({'message': 'Volunteer updated successfully'}, status=status.HTTP_200_OK)
                except Volunteer.DoesNotExist:
                    return Response({'error': 'Volunteer not found'}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({'error': 'ID required'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        

class TaskEdit(APIView):
    def put(self, request):
        if admin_access(request.data.get('token')):

            id = request.data.get('id')
            if not id:
                return Response({'error': 'ID required'}, status=status.HTTP_400_BAD_REQUEST)
            try:
                task = Task.objects.get(id=id)
            except Task.DoesNotExist:
                return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
            
            name = request.data.get('name')
            roll = request.data.get('roll')
            volunteer_id = request.data.get('volunteer_id')
            client_id = request.data.get('client_id')
            task_status = request.data.get('status')

            if name:
                task.name = name
            if roll:
                task.roll = roll
            if task_status:
                task.status = task_status

            if volunteer_id:
                try:
                    volunteer = Volunteer.objects.get(id=volunteer_id)
                    task.volunteers.set([volunteer])
                except Volunteer.DoesNotExist:
                    return Response({'error': 'Volunteer not found'}, status=status.HTTP_404_NOT_FOUND)

            if client_id:
                try:
                    client = Client.objects.get(id=client_id)
                    task.client = client
                except Client.DoesNotExist:
                    return Response({'error': 'Client not found'}, status=status.HTTP_404_NOT_FOUND)

            task.save()
            return Response({'message': 'Task updated successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
    

class SingleVolunteer(APIView):
    def get(self, request):
        if admin_access(request.data.get('token')):
            try:
                volunteer = Volunteer.objects.get(id=request.data.get('id'))
                volunteer_data = {
                    'id': volunteer.id,
                    'name': volunteer.name,
                    'roll': volunteer.roll,
                    'created_at': volunteer.created_at,
                    'tasks_pending': list(volunteer.tasks.filter(status='pending').values('id', 'name', 'roll', 'status')),
                    'tasks_completed': list(volunteer.tasks.filter(status='completed').values('id', 'name', 'roll', 'status'))
                }
                return Response(volunteer_data, status=status.HTTP_200_OK)
            except Volunteer.DoesNotExist:
                return Response({'error': 'Volunteer not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        

class SingleClient(APIView):
    def get(self, request):
        if admin_access(request.data.get('token')):
            try:
                if request.data.get('id') is not None:
                    client = Client.objects.get(id=request.data.get('id'))
                    client_data = {
                        'id': client.id,
                        'name': client.name,
                        'phone_number': client.phone_number,
                        'constituency': client.constituency,
                        'image': client.image.url if client.image else None,
                        'total_amount': client.total_amount,
                        'email' : client.email,
                        'created_at': client.created_at,
                        'tasks_pending': list(Task.objects.filter(client = request.data.get('id'), status='pending').values('id', 'name', 'roll', 'status')),
                        'tasks_completed': list(Task.objects.filter(client = request.data.get('id'), status='completed').values('id', 'name', 'roll', 'status'))
                    }
                    return Response(client_data, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'ID required'}, status=status.HTTP_400_BAD_REQUEST)
            except Client.DoesNotExist:
                return Response({'error': 'Client not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        

class SingleTask(APIView):
    def get(self, request):
        if admin_access(request.data.get('token')):
            try:
                if request.data.get('id') is not None:
                    task = Task.objects.get(id=request.data.get('id'))
                    task_data = {
                        'id': task.id,
                        'name': task.name,
                        'roll': task.roll,
                        'volunteers_count': task.volunteers.count(),
                        'created_at' : task.created_at,
                        'volunteers': list(task.volunteers.values('id', 'name', 'roll')),
                        'client': {'id' : task.client.id,
                                    'name': task.client.name} if task.client else None,
                        'status': task.status
                    }
                    return Response(task_data, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'ID required'}, status=status.HTTP_400_BAD_REQUEST)
            except Task.DoesNotExist:
                return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)




        
