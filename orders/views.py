from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import generic
from django.contrib.auth.models import Permission, User
# Create your views here.
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from .models import Employee
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

def  index(request):
    return render(request, 'orders/login.html')

#use this to check if logged else redirect to login url
@login_required 
def check_web(request):
    try:
        emp = request.user
        employee = Employee.objects.get(user=emp)
        if employee is not None:
             print(employee.employee_type)
        else:
            print('redirect')    
        data = {'Employee': 'success'}
        return JsonResponse(data)  

    except Exception as e:
        print(e) 
        data = {'Employee': 'error'}
        print('User not found')
        return JsonResponse(data)    


def login_web(request):
    rusername = request.POST.get('username')
    rpassword = request.POST.get('password')
    print(rusername)
    print(rpassword)
    user = authenticate(request, username=rusername, password=rpassword)
    if user is not None:
        login(request, user)
        print(user.groups.all()[:1].get().name)#can use this get the group of user
        
        data = {'Employee': 'hi'}
        return render(request, 'orders/register.html')
    else:
        data = {'Employee': 'error'}
        print('User not found')
        return JsonResponse(data)

#logging out a logged in user
def logout_view(request):
     logout(request)            
