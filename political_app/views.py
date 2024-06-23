import string, secrets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from political_app.models import Volunteer, Task, Client, Admin
from .utils import hash_password, check_password



class Home(APIView): 
    def get(request):
        if request.data.get('role') == 'admin' or 'volunteer':
            return Response("welcome to the application")


class Login(APIView):
    def post(self, request):
        user_name = request.data.get('user_name')
        password = request.data.get('password')
        
        if not user_name or not password:
            return Response({'error': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            admin = Admin.objects.get(email=user_name)
            if check_password(admin.password, password):
                return Response({'message': 'Login successful',
                                 'admin': admin.name,
                                 'role': 'admin'}, status=status.HTTP_200_OK)
        except Admin.DoesNotExist:
            try:
                volunteer = Volunteer.objects.get(email=user_name)
                if check_password(volunteer.password, password):
                    return Response({'message': 'Login successful',
                                     'volunteer': volunteer.name,
                                     'role': 'volunteer'}, status=status.HTTP_200_OK)
            except Volunteer.DoesNotExist:
                return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)


class ResetPassword(APIView):
    def post(self, request):
        user_name = request.data.get('user_name')
        password = request.data.get('password')
        new_password = request.data.get('new_password')
        if user_name and password:
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
            return JsonResponse({'error': 'Username and password are required.'}, status=400)


class AdminCreate(APIView):
    def post(self, request):
        if request.data.get('role') == 'admin':
            name = request.data.get('name')
            phone_number = request.data.get('phone_number')
            email = request.data.get('email')
            alphabet = string.ascii_letters + string.digits
            password = ''.join(secrets.choice(alphabet) for _ in range(12))
            if name and email and password:
                admin = Admin.objects.create(name=name, phone_number=phone_number, email=email, password = hash_password(password))
                if admin:
                    subject = 'Admin Account Created'
                    message = f'''Hello {name},

    Your account has been created with user_name {email} and password is  {password}
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
                    return JsonResponse({'message': f'Admin created with name : {name}'}, status = 200)
                else:
                    return JsonResponse({'message': f'Some error occured'}, status = 400)
            else:
                    return JsonResponse({'message': f'name must be provided'}, status = 400)


class VolunteerCreate(APIView):
    def post(self, request):
        if request.data.get('role') == 'admin':
            name = request.data.get('name')
            roll = request.data.get('roll')
            phone_number = request.data.get('phone_number')
            email = request.data.get('email')
            alphabet = string.ascii_letters + string.digits
            password = ''.join(secrets.choice(alphabet) for _ in range(12))
            
            if name and email and password:
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
                return JsonResponse({'error': 'Name and roll parameters are required.'}, status=400)

class TaskCreate(APIView):
    def post(self, request):
        if request.data.get('role') == 'admin' or 'volunteer':
            name = request.data.get('name')
            roll = request.data.get('roll')
            volunteer_id = request.data.get('volunteer_id')
            
            if not name or not roll:
                return Response({'error': 'Name, roll parameters are required.'}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                if volunteer_id:
                    volunteer = Volunteer.objects.get(id=volunteer_id)
                else:
                    volunteer = None
            except Volunteer.DoesNotExist:
                volunteer = None
            
            task = Task.objects.create(name=name, roll=roll, volunteer=volunteer)
            return Response({'message': f'Task created: {task.name}'}, status=status.HTTP_201_CREATED)


class ClientCreate(APIView):
    def post(self, request):
        if request.data.get('role') == 'admin':
            name = request.data.get('name')
            phone_number = request.data.get('phone_number')
            constituency = request.data.get('constituency')
            task_id = request.data.get('task_id')
            image = request.FILES.get('image')

            if not all([name, phone_number]):
                return Response({'error': 'Name, phone number parameters are required.'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                if task_id:
                    task_instance = Task.objects.get(id=task_id)
                else:
                    task_instance = None
            except Task.DoesNotExist:
                task_instance = None

            client = Client.objects.create(
                name=name,
                phone_number=phone_number,
                constituency=constituency,
                image=image,
                task=task_instance
            )

            return Response({'message': f'Client created: {client.name}'}, status=status.HTTP_201_CREATED)


class VolunteerList(APIView):
    def get(self, request):
        if request.data.get('role') == 'admin':
            volunteers_instances = Volunteer.objects.all()
            volunteers = [
                {
                    'id': volunteer.id,
                    'name': volunteer.name,
                    'roll': volunteer.roll
                }
                for volunteer in volunteers_instances
            ]
            return Response(volunteers, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

class TaskList(APIView):
    def get(self, request):
        if request.data.get('role') == 'admin' or 'volunteer':
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

class ClientList(APIView):
    def get(self, request):
        if request.data.get('role') == 'admin':
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