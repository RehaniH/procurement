from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.views import generic
from django.contrib.auth.models import Permission, User
# Create your views here.
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from .models import Employee

def  index(request):
    return render(request, 'orders/login.html')

def login_web(request):
    try:
        email = request.POST['username']
        password = request.POST['password']
        employee = Employee.objects.get(email=email, password=password)
        if employee is not None:
             print(employee.type)
        else:
            print('redirect')     
    except Exception as e:
        print(e)     
