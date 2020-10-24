"""The class for logging to server"""
import logging

from django.views.generic import View
from django.http import JsonResponse
from django.http import HttpResponseRedirect

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from orders.serializers import DeliveryLogSerializer, StockSerializer, requestOrdersSerializer
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from django.shortcuts import render


from django.contrib.auth import authenticate, login, logout
from django.views import generic
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from rest_framework import generics
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.db.utils import IntegrityError
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from orders.models import (
    Employee, Rule1, Rule2, Rule3, Pending_orders,  DeliveryLog, Item, OrderStatus, RequestOrders, Site, Stock, Orders,
    Item, ItemPrices, Supplier, RequestOrders)

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


def update_purchase_order(request, request_id, order_id ):
    """update a drafted purchase order"""
    success_status = 0  # success status is initially set to 0
    try:
        item_price_id = request.POST.get('item_price_id', None)
        order_request = RequestOrders.objects.get(pk=request_id)
        active = True
        item_price = ItemPrices.objects.get(pk=item_price_id)
        supplier = item_price.supplier
        price = item_price.price
        status = OrderStatus.objects.get(abbv="PEND")

        #saving newly added information to existing order object
        order = Orders.objects.get(pk=order_id)
        order.price = price
        order.status = status
        order.active = active
        order.supplier = supplier
        order.item = order_request.item
        order.quantity = order_request.quantity
        order.quantity_type = order_request.quantity_type
        order.save()
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

@method_decorator(login_required, name='dispatch')
class Ruleslist(generic.ListView):
    """Add new Rules to system or activate or deactivate them"""
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

@method_decorator(login_required, name='dispatch')
class Approvals(generic.ListView):
    """Get Management staff approval"""
    model = Pending_orders
    template_name = 'rules_management/approval.html'
    context_object_name = 'approvals'
    

    def get_context_data(self, **kwargs):
        u=self.request.user
        print(u)
        context = super(Approvals, self).get_context_data(**kwargs)
        context.update({
            'p_orders_r1': Pending_orders.objects.filter(approved=0,Ruletype1=1),
            'p_orders_r2': Pending_orders.objects.filter(approved=0,Ruletype2=1),
            'p_orders_r3': Pending_orders.objects.filter(approved=0,Ruletype3=2),
            'p_orders_ed': Pending_orders.objects.filter(approved=0,EditRequest=1),
            'p_orders_del': Pending_orders.objects.filter(approved=0,DeleteRequest=1),
            
        })

        return context

def manage_approvals(request):
    """Filter orders according to Company Rules"""

    rule_1=Rule1.objects.filter(active_status=True)
    rule_2=Rule2.objects.filter(active_status=True)
    rule_3=Rule3.objects.filter(active_status=True)
    pending_requests=Orders.objects.filter(status__abbv="PEND")
    edit_requests=Orders.objects.filter(status__abbv="RQEDI")
    delete_requests=Orders.objects.filter(status__abbv="RQDEL")
    is_rule1=False
    is_rule2=False

    for object in delete_requests:
        p,obj_not_exist=Pending_orders.objects.get_or_create(orderno=object)
        print(p.id)
        if  obj_not_exist:
            p.DeleteRequest=1
            p.save()
          
        else:
            obj_exist=Pending_orders.objects.get(orderno_id=object.id)
            obj_exist.DeleteRequest=1
            obj_exist.save()

    for object in edit_requests:
        p,obj_not_exist=Pending_orders.objects.get_or_create(orderno=object)

        if  obj_not_exist:
            p.EditRequest=1
            p.save()

        else:
            obj_exist=Pending_orders.objects.get(orderno_id=object.id)
            obj_exist.EditRequest=1
            obj_exist.save()

    for object in pending_requests:
        is_rule1=False
        is_rule2=False

        if rule_1:
            for rule in rule_1:
                if(object.item.id==rule.item.id):
                    is_rule1=True
                    p,obj_not_exist=Pending_orders.objects.get_or_create(orderno=object)

                    if  obj_not_exist:
                        p.Ruletype1=1
                        p.save()

                    else:
                        obj_exist=Pending_orders.objects.get(orderno_id=object.id)
                        obj_exist.Ruletype1=1
                        obj_exist.save()
        if rule_2:
            for rule in rule_2:
                
                if(object.price*object.quantity>=rule.price_limit):

                    is_rule2=True
                    p,obj_not_exist=Pending_orders.objects.get_or_create(orderno=object)

                    if  obj_not_exist:
                        p.Ruletype2=1
                        p.save()

                    else:
                        obj_exist=Pending_orders.objects.get(orderno_id=object.id)
                        obj_exist.Ruletype2=1
                        obj_exist.save()
                        

        
        if(is_rule1==True and is_rule2==True):
            p,obj_not_exist=Pending_orders.objects.get_or_create(orderno=object)

            if  obj_not_exist:
                p.Ruletype3=2
                p.save()

            else:
                obj_exist=Pending_orders.objects.get(orderno_id=object.id)
                obj_exist.Ruletype3=2
                obj_exist.save()

        elif(is_rule1==False and is_rule2==False):
            order_approved=Orders.objects.get(id__exact=object.id)
            status = OrderStatus.objects.get(abbv="APPV")
            order_approved.status=status
            order_approved.save()


            
            

    data = {
            'postitive': 2
        }
    return JsonResponse(data)


    



class AddItemRule(View):
    """Add new Item Rule"""
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
    """update status of item rule"""
    status_id = request.GET.get('id', None)
    print(status_id)
    obj = Rule1.objects.get(id=status_id)
    realstatus = obj.active_status

    if(realstatus == True):
        obj.active_status = 0
        obj.save()
        data = {
            'is_taken': 2
        }
        return JsonResponse(data)

    else:

        obj.active_status = 1
        obj.save()
        data = {
            'is_taken': 1
        }
        return JsonResponse(data)


class AddPriceRule(View):
    """Add new Price limit"""

    def get(self, request):

        ruleid = request.GET.get('ruleid', None)
        price = request.GET.get('priceLimit', None)

        

        obj = Rule2.objects.get(id=ruleid)
        obj.price_limit = price
        obj.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def getPriceRule(request):
    """change price limit status """

    status_id = request.GET.get('id', None)
    obj = Rule2.objects.get(id=status_id)
    realstatus = obj.active_status

    if(realstatus == True):
        obj.active_status = 0
        obj.save()
        data = {
            'is_taken': 2
        }
        return JsonResponse(data)

    else:

        obj.active_status = 1
        obj.save()
        data = {
            'is_taken': 1
        }
        return JsonResponse(data)


class AddlevelRule(View):
    """Add new Level rule"""

    def get(self, request):

        ruleid = request.GET.get('ruleid1', None)
        level = request.GET.get('level', None)

        

        obj = Rule3.objects.get(id=ruleid)
        obj.level = level
        obj.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def getlevelRule(request):
    """Change level rule status"""
    status_id = request.GET.get('id', None)
    obj = Rule3.objects.get(id=status_id)
    realstatus = obj.active_status

    if(realstatus == True):
        obj.active_status = 0
        obj.save()
        data = {
            'is_taken': 2
        }
        return JsonResponse(data)

    else:

        obj.active_status = 1
        obj.save()
        data = {
            'is_taken': 1
        }
        return JsonResponse(data)


def status_rule_one(request):
    """Approve or decline according to item rule"""
    status_id = request.GET.get('id', None)
    status = request.GET.get('status', None)
    
    if(status == '1'):
        obj = Pending_orders.objects.get(id=status_id)
        obj.Ruletype1=0
        obj.save()

        suitable_object=Pending_orders.objects.get(
        id=status_id,
        Ruletype1=0,
        Ruletype2=0,
        Ruletype3=0,
        DeleteRequest=0,
        EditRequest=0,
        )


        if suitable_object:
            suitable_object.approved=1
            suitable_object.save()

            order_approved=Orders.objects.get(id__exact=suitable_object.orderno_id)
            status = OrderStatus.objects.get(abbv="APPV")
            order_approved.status=status
            order_approved.save()


        data = {
            'status': True
        }
        return JsonResponse(data)


    else:
        obj=Pending_orders.objects.get(id=status_id)
        obj.approved=2
        obj.save()

        order_declined=Orders.objects.get(id__exact=obj.orderno_id)
        status = OrderStatus.objects.get(abbv="DECL")
        order_declined.status=status
        order_declined.active=False
        order_declined.save()

        data = {
            'status': False
        }
        return JsonResponse(data)
        
def status_rule_two(request):
    """Approve or decline according to price limit rule"""
    status_id = request.GET.get('id', None)
    status = request.GET.get('status', None)
    
    if(status == '1'):
        obj = Pending_orders.objects.get(id=status_id)
        obj.Ruletype2=0
        obj.save()

        suitable_object=Pending_orders.objects.get(
        id=status_id,
        Ruletype1=0,
        Ruletype2=0,
        Ruletype3=0,
        DeleteRequest=0,
        EditRequest=0,
        )


        if suitable_object:
            suitable_object.approved=1
            suitable_object.save()

            order_approved=Orders.objects.get(id__exact=suitable_object.orderno_id)
            status = OrderStatus.objects.get(abbv="APPV")
            order_approved.status=status
            order_approved.save()


        data = {
            'status': True
        }
        return JsonResponse(data)


    else:
        obj=Pending_orders.objects.get(id=status_id)
        obj.approved=2
        obj.save()

        order_declined=Orders.objects.get(id__exact=obj.orderno_id)
        status = OrderStatus.objects.get(abbv="DECL")
        order_declined.status=status
        order_declined.active=False
        order_declined.save()


        data = {
            'status': False
        }
        return JsonResponse(data)

def status_rule_three(request):
    """Approve or decline according to levels"""
    status_id = request.GET.get('id', None)
    status = request.GET.get('status', None)
    
    if(status == '1'):
        obj = Pending_orders.objects.get(id=status_id)
        obj.Ruletype3=0
        obj.save()

        suitable_object=Pending_orders.objects.get(
        id=status_id,
        Ruletype1=0,
        Ruletype2=0,
        Ruletype3=0,
        DeleteRequest=0,
        EditRequest=0,
        )

        if suitable_object:
            suitable_object.approved=1
            suitable_object.save()

            order_approved=Orders.objects.get(id__exact=suitable_object.orderno_id)
            status = OrderStatus.objects.get(abbv="APPV")
            order_approved.status=status
            order_approved.save()

        data = {
            'status': True
        }
        return JsonResponse(data)


    else:
        obj=Pending_orders.objects.get(id=status_id)
        obj.approved=2
        obj.save()

        order_declined=Orders.objects.get(id__exact=obj.orderno_id)
        status = OrderStatus.objects.get(abbv="DECL")
        order_declined.status=status
        order_declined.active=False
        order_declined.save()


        data = {
            'status': False
        }
        return JsonResponse(data)

def status_edit_requests(request):
    """Approve or decline according to Edit Requests"""
    status_id = request.GET.get('id', None)
    status = request.GET.get('status', None)
    if(status == '1'):
        obj = Pending_orders.objects.get(id=status_id)
        obj.EditRequest=0
        obj.save()

        order_approved=Orders.objects.get(id__exact=obj.orderno_id)
        status = OrderStatus.objects.get(abbv="PEND")
        order_approved.status=status
        order_approved.save()

        data = {
            'status': True
        }
        return JsonResponse(data)


    else:
        obj=Pending_orders.objects.get(id=status_id)
        obj.approved=2
        obj.save()

        order_declined=Orders.objects.get(id__exact=obj.orderno_id)
        status = OrderStatus.objects.get(abbv="DECL")
        order_declined.status=status
        order_declined.active=False
        order_declined.save()


        data = {
            'status': False
        }
        return JsonResponse(data)

def status_delete_requests(request):
    """Approve or decline according to Delete Requests"""
    status_id = request.GET.get('id', None)
    status = request.GET.get('status', None)
    if(status == '1'):
        obj = Pending_orders.objects.get(id=status_id)
        obj.DeleteRequest=0
        obj.save()

        order_approved=Orders.objects.get(id__exact=obj.orderno_id)
        status = OrderStatus.objects.get(abbv="DELET")
        order_approved.status=status
        order_approved.save()

        data = {
            'status': True
        }
        return JsonResponse(data)


    else:
        obj=Pending_orders.objects.get(id=status_id)
        obj.approved=2
        obj.save()

        order_declined=Orders.objects.get(id__exact=obj.orderno_id)
        status = OrderStatus.objects.get(abbv="DECL")
        order_declined.status=status
        order_declined.active=False
        order_declined.save()


        data = {
            'status': False
        }
        return JsonResponse(data)