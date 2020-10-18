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


def create_purchase_order(request, pk):
    """create or draft a purchase order from an order request"""
    success_status = 0  # success status is initially set to 0
    try:
        item_price_id = request.POST.get('item_price_id', None)
        order_request = RequestOrders.objects.get(pk=pk)
        supplier = None
        item_price = None
        active = False
        order_item = order_request.item
        if item_price_id is not None:
            item_price = ItemPrices.objects.get(pk=item_price_id)
            supplier = item_price.supplier
            active = True
        # set the order status to Pending
        status = OrderStatus.objects.get(abbv="PEND")
        # if the price is not set, the order would be saved as a draft
        price = (item_price.price if (item_price is not None) else 0)

        order = Orders.objects.create(
            item=order_item,
            quantity=order_request.quantity,
            quantity_type=order_request.quantity_type,
            price=price,
            delivery_date=order_request.expected_date,
            site=order_request.site,
            status=status,
            request=order_request,
            active=active,
            supplier=supplier
        )
        data = {
            'id': order.id,
            'status': order.status.status,
            'item': order.item.name,
        }
        success_status = 1
    except ObjectDoesNotExist as ex:
        logger.exception(ex)
        data = {
            'error_message': 'The required information does not exists',
        }
    except Exception as exception:
        logger.exception(exception)
        data = {
            'error_message': 'Unable to process request',
        }
    finally:
        data['success_stat'] = success_status
        return JsonResponse(data)


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
        itemid = request.GET.get('itemid', None)

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
    realstatus = obj.active_status

    if(realstatus == True):
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

        ruleid = request.GET.get('ruleid', None)
        price = request.GET.get('priceLimit', None)

        print(price)
        print(ruleid)

        obj = Rule2.objects.get(id=ruleid)
        obj.price_limit = price
        obj.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def getPriceRule(request):
    status_id = request.GET.get('id', None)
    print(status_id)
    obj = Rule2.objects.get(id=status_id)
    realstatus = obj.active_status

    if(realstatus == True):
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

        ruleid = request.GET.get('ruleid1', None)
        level = request.GET.get('level', None)

        print(level)
        print(ruleid)

        obj = Rule3.objects.get(id=ruleid)
        obj.level = level
        obj.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def getlevelRule(request):
    status_id = request.GET.get('id', None)
    print(status_id)
    obj = Rule3.objects.get(id=status_id)
    realstatus = obj.active_status

    if(realstatus == True):
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


