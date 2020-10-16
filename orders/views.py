from django.views.generic import ListView
from django.views.generic import View
from django.http import JsonResponse

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.views import generic
from django.contrib.auth.models import Permission, User
# Create your views here.
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from .models import Employee, Rule1, Rule2, Rule3, Pending_orders


def index(request):
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


class Ruleslist(generic.ListView):
    model = Pending_orders
    template_name = 'rules_management/rulesList.html'
    context_object_name = 'listdata'

    def get_context_data(self, **kwargs):
        context = super(Ruleslist, self).get_context_data(**kwargs)
        context.update({
            'rule1': Rule1.objects.select_related('item'),
            'rule2': Rule2.objects.all(),
            'rule3': Rule3.objects.all(),
            # 'more_context': Model.objects.all(),
        })

        return context

    # return render(request, 'rules_management/rulesList.html')
