"""The class for logging to server"""
import logging

from django.shortcuts import render  # , redirect
from django.utils.datastructures import MultiValueDictKeyError
from django.views.generic import ListView
from django.views.generic import View
from django.http import JsonResponse
from django.http import HttpResponseRedirect

from django.shortcuts import render
# andrew
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from orders.models import DeliveryLog, Item, OrderStatus, RequestOrders, Site, Stock, Orders
from orders.serializers import DeliveryLogSerializer, StockSerializer, requestOrdersSerializer
from rest_framework.decorators import api_view

from django.contrib.auth import authenticate, login, logout
from django.views import generic
from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from orders.models import Employee
from rest_framework import generics
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from orders.models import Employee, RequestOrders, Item, ItemPrices, Supplier, Orders, OrderStatus, Site
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.db.utils import IntegrityError
from orders.models import Employee, Rule1, Rule2, Rule3, Pending_orders, Item

logger = logging.getLogger(__name__)



def index(request):
    """Index page of the application."""
    return render(request, 'orders/login.html')


def login_web(request):
    """Authenticating a login request."""
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        user_group = user.groups.all()[:1].get().name
        # user.groups.all()[:1].get().name #can use this get the group of user

        if(user_group == "Manager" or user_group == "Supervisor"):
            # replace this with your dashboard
            return render(request, 'orders/register.html')
        elif(user_group == "Accounting Staff"):
            return render(request, 'accounting/dashboard.html')
        else:
            return render(request, 'orders/login.html')

    else:
        logger.error("User is not found: " + username + "  = " + password)
        data = {'Employee': 'error'}
        return JsonResponse(data)

# logging out a logged in user


def logout_view(request):
    """Logging out a logged in user."""
    logout(request)
    return render(request, 'orders/login.html')




