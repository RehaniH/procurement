"""The class for logging to server"""
import logging

from django.shortcuts import render 
from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from orders.models import Item

logger = logging.getLogger(__name__)



def index(request):
    """Index page of the application."""
    return render(request, 'orders/login.html')


def login_web(request):
    """Authenticating a login request."""
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        user_group = user.groups.all()[:1].get().name
        # user.groups.all()[:1].get().name #can use this get the group of user

        if(user_group == "Manager" or user_group == "Supervisor"):
            return redirect('rulelist')
        elif(user_group == "Accounting Staff"):
            context = {'item_list': Item.objects.all() }
            return render(request, 'accounting/items-catalog.html', context)
        else:
            return render(request, 'orders/login.html')

    else:
        logger.error("User is not found: " + username + "  = " + password)
        context = {
            'login_error': 'username or password is incorrect.'
        }
        return render(request, 'orders/login.html', context)


def logout_view(request):
    """Logging out a logged in user."""
    logout(request)
    return render(request, 'orders/login.html')




