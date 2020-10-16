from django.views.generic import ListView
from django.views.generic import View
from django.http import JsonResponse
from django.http import HttpResponseRedirect

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.views import generic
from django.contrib.auth.models import Permission, User
# Create your views here.
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from .models import Employee, Rule1, Rule2, Rule3, Pending_orders,Item


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
            'items': Item.objects.all(),
            # 'more_context': Model.objects.all(),
        })

        return context

    # return render(request, 'rules_management/rulesList.html')


class AddItemRule(View):
    def get(self, request):
        rulecode = request.GET.get('rulecode', None)
        itemid =request.GET.get('itemid', None)

        print(rulecode)
        print(itemid)

        obj = Rule1.objects.create(
            rule_code=rulecode,
            item_id=itemid,
            active_status=1
        )

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def getItemRule(request):

    status_id = request.GET.get('id', None)    
    print(status_id)    
    obj = Rule1.objects.get(id=status_id)
    realstatus=obj.active_status

    if(realstatus==True):
        print('inside true')
        obj.active_status = 0
        obj.save()
        data = {
        'is_taken': 2
        }
        return JsonResponse(data)

    else:
        print('inside true')

        obj.active_status = 1
        obj.save()
        data = {
        'is_taken': 1
        }
        return JsonResponse(data)


class AddPriceRule(View):
    def get(self, request):

        ruleid= request.GET.get('ruleid', None)
        price= request.GET.get('priceLimit', None)

        print(price)
        print(ruleid)
    
        obj = Rule2.objects.get(id=ruleid)
        obj.price_limit=price
        obj.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def getPriceRule(request):
    status_id = request.GET.get('id', None)    
    print(status_id)    
    obj = Rule2.objects.get(id=status_id)
    realstatus=obj.active_status

    if(realstatus==True):
        print('inside true')
        obj.active_status = 0
        obj.save()
        data = {
        'is_taken': 2
        }
        return JsonResponse(data)

    else:
        print('inside true')

        obj.active_status = 1
        obj.save()
        data = {
        'is_taken': 1
        }
        return JsonResponse(data)


class AddlevelRule(View):
    def get(self, request):

        ruleid= request.GET.get('ruleid1', None)
        level= request.GET.get('level', None)

        print(level)
        print(ruleid)
    
        obj = Rule3.objects.get(id=ruleid)
        obj.level=level
        obj.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def getlevelRule(request):
    status_id = request.GET.get('id', None)    
    print(status_id)    
    obj = Rule3.objects.get(id=status_id)
    realstatus=obj.active_status

    if(realstatus==True):
        print('inside true')
        obj.active_status = 0
        obj.save()
        data = {
        'is_taken': 2
        }
        return JsonResponse(data)

    else:
        print('inside true')

        obj.active_status = 1
        obj.save()
        data = {
        'is_taken': 1
        }
        return JsonResponse(data)



        



