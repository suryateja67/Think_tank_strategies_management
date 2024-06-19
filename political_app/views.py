from django.shortcuts import render
from political_app.models import Volunteer, Task, Client, Admin
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .utils import hash_password, check_password

# Create your views here.
def home(request):
    return HttpResponse("welcome to the application")

@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            admin = Admin.objects.get(email=username)
            if admin and check_password(admin.password, password):
                return JsonResponse({'message': 'Login successful',
                                    'admin': admin.name,
                                    'role': admin.role}, status = 200)
            elif not admin:
                volunteer = Volunteer.objects.get(email=username)
                if volunteer and check_password(volunteer.password, password):
                    return JsonResponse({'message': 'Login successful',
                                        'volunteer': volunteer.name,
                                        'role': volunteer.role}, status = 200)
            else:
                return JsonResponse({'error': 'Invalid credentials.'}, status=401)
        else:
            return JsonResponse({'error': 'Username and password are required.'}, status=400)


@csrf_exempt
def admin(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if name:
            admin = Admin.objects.create(name=name, phone_number=phone_number, email=email, password = hash_password(password))
            print(admin)
            if admin:
                return JsonResponse({'message': f'Admin created with name : {admin.name}'}, status = 200)
            else:
                return JsonResponse({'message': f'Some error occured'}, status = 400)
        else:
                return JsonResponse({'message': f'name must be provided'}, status = 400)


@csrf_exempt
def volunteer(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        roll = request.POST.get('roll')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if name:
            volunteer = Volunteer.objects.create(name=name, roll=roll, phone_number=phone_number, email=email, password = hash_password(password))

            return JsonResponse({'message': f'Volunteer created with name : {volunteer.name}'})
        else:
            return JsonResponse({'error': 'Name and roll parameters are required.'}, status=400)

@csrf_exempt
def task(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        roll = request.POST.get('roll')
        volunteer_id = request.POST.get('volunteer_id')
        if name:
            volunteer = Volunteer.objects.get(id=volunteer_id)
            task = Task.objects.create(name=name, roll=roll, volunteer=volunteer)
            return JsonResponse({'message': f'Task created: {task.name}'})
        else:
            return JsonResponse({'error': 'Name, roll and volunteer_id parameters are required.'}, status=400)



@csrf_exempt
def client(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone_number = request.POST.get('phone_number')
        constituency = request.POST.get('constituency')
        task_id = request.POST.get('task_id')
        image = request.FILES.get('image')

        try:
            task_instance = Task.objects.get(id=task_id)
            client = Client.objects.create(
                name=name, 
                phone_number=phone_number, 
                constituency=constituency, 
                image=image, 
                task=task_instance
            )
            client.save()
            return JsonResponse({'message': f'Client created: {client.name}'})
        except Task.DoesNotExist:
            return JsonResponse({'error': 'Task not found'}, status=404)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


def volunteer_list(self):
    volunteers_instances = Volunteer.objects.all()
    volunteers = []
    for volunteer in volunteers_instances:
        volunteers.append({
            'id': volunteer.id,
            'name': volunteer.name,
            'roll': volunteer.roll
        })
    return JsonResponse(volunteers)


def task_list(self):
    tasks_instances = Task.objects.all()
    tasks = []
    for task in tasks_instances:
        tasks.append({
            'id': task.id,
            'name': task.name,
            'roll': task.roll
        })
    return JsonResponse(tasks)


def client_list(self):
    clients_instances = Client.objects.all()
    clients = []
    for client in clients_instances:
        clients.append({
            'id': client.id,
            'name': client.name,
            'phone_number': client.phone_number,
            'constituency': client.constituency,
            'image': client.image
        })
    return HttpResponse(clients)   