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
from .models import DeliveryLog, Item, OrderStatus, RequestOrders, Site, Stock, Orders
from .serializers import DeliveryLogSerializer, StockSerializer, requestOrdersSerializer
from rest_framework.decorators import api_view

from django.contrib.auth import authenticate, login, logout
from django.views import generic
from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from .models import Employee
from rest_framework import generics
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Employee, RequestOrders, Item, ItemPrices, Supplier, Orders, OrderStatus, Site
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.db.utils import IntegrityError
from .models import Employee, Rule1, Rule2, Rule3, Pending_orders, Item

logger = logging.getLogger(__name__)


def index(request):
    """Index page of the application."""
    return render(request, 'orders/login.html')

# sample
# use this to check if logged else redirect to login url


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

# REQUEST ORDER


@api_view(['GET', 'POST', 'DELETE'])
def requestOrder_list(request):
    if request.method == 'GET':
        requestOrders = RequestOrders.objects.all()
        requestOrder_Serializer = requestOrdersSerializer(
            requestOrders, many=True)
        return JsonResponse(requestOrder_Serializer.data, safe=False)

    elif request.method == 'POST':
        reqorder_data = JSONParser().parse(request)
        print(reqorder_data)
        itemid = reqorder_data['item']
        print(itemid)
        quantityy = reqorder_data['quantity']
        print(quantityy)
        expected_datee = reqorder_data['expected_date']
        commentt = reqorder_data['comment']
        qnty_typee = reqorder_data['quantity_type']
        print(qnty_typee)
        itemm = Item.objects.get(name=itemid)
        print(itemm)
        statusobj = OrderStatus.objects.get(status__iexact='pending')
        print(statusobj)
        # siteobj=Site.objects.get()
        obj = RequestOrders.objects.create(
            item=itemm,
            quantity=quantityy,
            comment=commentt,
            status=statusobj,
            expected_date=expected_datee,
            quantity_type=qnty_typee



        )

        req_serializer = requestOrdersSerializer(data=reqorder_data)
        if req_serializer.is_valid():
            #     req_serializer.save()
            return JsonResponse(req_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(req_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def reqOrder_detail(request, pk):
    try:
        requestOrder = RequestOrders.objects.get(pk=pk)
    except RequestOrders.DoesNotExist:
        return JsonResponse({'message': 'The Requested order does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        request_serializer = requestOrdersSerializer(requestOrder)
        return JsonResponse(request_serializer.data)

    elif request.method == 'PUT':
        reqorder_data = JSONParser().parse(request)
        quantityy = reqorder_data['quantity']
        print(quantityy)
        expected_datee = reqorder_data['expected_date']
        commentt = reqorder_data['comment']
        obj = RequestOrders.objects.update(
            expected_date=expected_datee,
            quantity=quantityy,
            comment=commentt
        )

        request_serializer = requestOrdersSerializer(
            requestOrder, data=reqorder_data)
        if request_serializer.is_valid():
            # request_serializer.save()
            return JsonResponse(request_serializer.data)
        return JsonResponse(request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        requestOrder.delete()
        return JsonResponse({'message': 'request order was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


# DELIVERY LOG
@api_view(['GET', 'POST', 'DELETE'])
def DeliveryLog_list(request):
    if request.method == 'GET':
        Delivery_Log = DeliveryLog.objects.all()
        DeliveryLog_Serializer = DeliveryLogSerializer(Delivery_Log, many=True)
        return JsonResponse(DeliveryLog_Serializer.data, safe=False)

    elif request.method == 'POST':
        DeliveryLog_data = JSONParser().parse(request)
        print(DeliveryLog_data['purchased_orders'])
        id = DeliveryLog_data['purchased_orders']
        order = Orders.objects.values_list('item', flat=True).get(pk=id)
        stock = Stock.objects.get(item_id=order)

        stock.quantity += DeliveryLog_data['quantity']
        orderobj = Orders.objects.get(pk=id)
        orderobj.remaining_quantity -= DeliveryLog_data['quantity']
        if(orderobj.remaining_quantity <= 0):
            orderobj.status = OrderStatus.objects.get(status='completed')
        orderobj.save()

        stock.save()

        print(stock)

        Dellog_serializer = DeliveryLogSerializer(data=DeliveryLog_data)
        # order id -> order record-> item(4)=stock.item(4)
        if Dellog_serializer.is_valid():
            Dellog_serializer.save()
            # print(Dellog_serializer.data)
            # dellog_item=Dellog_serializer.data['item']
            # Update_Stock=Stock.objects.filter(item_id=dellog_item)
            # Stock_serializer = StockSerializer(DeliveryLog_data, data=Update_Stock)

            return JsonResponse(Dellog_serializer.data, status=status.HTTP_201_CREATED)

        return JsonResponse(Dellog_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def DeliveryLog_detail(request, pk):
    try:
        Delivery_log = DeliveryLog.objects.get(pk=pk)
    except DeliveryLog.DoesNotExist:
        return JsonResponse({'message': 'The Deliverylog order does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        DeliveryLog_serializer = DeliveryLogSerializer(Delivery_log)
        return JsonResponse(DeliveryLog_serializer.data)

    elif request.method == 'PUT':
        DeliveryLog_data = JSONParser().parse(request)
        Deliverylog_serializer = DeliveryLogSerializer(
            Delivery_log, data=DeliveryLog_data)
        if Deliverylog_serializer.is_valid():
            Deliverylog_serializer.save()
            return JsonResponse(Deliverylog_serializer.data)
        return JsonResponse(Deliverylog_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        Delivery_log.delete()
        return JsonResponse({'message': 'Deliverylog was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

# Stock


@api_view(['GET', 'POST', 'DELETE'])
def Stock_list(request):
    if request.method == 'GET':
        Stocks = Stock.objects.all()
        Stock_Serializer = StockSerializer(Stocks, many=True)
        return JsonResponse(Stock_Serializer.data, safe=False)

    elif request.method == 'POST':
        stock_data = JSONParser().parse(request)
        print(stock_data)
        itemid = stock_data['item']
        print(itemid)
        quantityy = stock_data['quantity']
        print(quantityy)
        quantity_typee = stock_data['quantity_type']
        reorder_levell = stock_data['reorder_level']
        itemm = Item.objects.get(name=itemid)
        print(itemm)

        obj = Stock.objects.create(
            item=itemm,
            quantity=quantityy,
            quantity_type=quantity_typee,
            reorder_level=reorder_levell
        )
        req_serializer = StockSerializer(data=stock_data)
        if req_serializer.is_valid():
            #     req_serializer.save()
            return JsonResponse(req_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(req_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def Stock_detail(request, pk):
    try:
        Stocks = Stock.objects.get(pk=pk)
    except Stock.DoesNotExist:
        return JsonResponse({'message': 'The stock does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        Stock_serializer = StockSerializer(Stock)
        return JsonResponse(Stock_serializer.data)

    elif request.method == 'PUT':
        Stock_data = JSONParser().parse(request)
        print(Stock_data)
        qnty = Stock_data['quantity']
        print(Stock_data['item'])
        Item_id = Stock_data['item']
        orderobj = Item.objects.get(pk=Item_id)
        statusobj = OrderStatus.objects.get(status__iexact='reorder item')

        print(orderobj)
        if(qnty <= Stocks.reorder_level):
            obj = RequestOrders.objects.create(
                item=orderobj,
                status=statusobj,
                auto_genarated=True

            )

        Stock_serializer = StockSerializer(Stocks, data=Stock_data)
        if Stock_serializer.is_valid():
            # Stock_serializer.save()
            return JsonResponse(Stock_serializer.data)
        return JsonResponse(Stock_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        Stocks.delete()
        return JsonResponse({'message': 'Stock was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


def index(request):
    return render(request, 'orders/login.html')

        return JsonResponse(data)

#login - authentication


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


class ViewRequests(generic.ListView):
    """"View a list of order requests generated by the site manager."""
    model = RequestOrders
    template_name = 'accounting/requests.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sites_list'] = Site.objects.all()
        return context


class ViewItems(generic.ListView):
    """View a list of saved catalog items."""
    model = Item
    template_name = 'accounting/items-catalog.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['itemprices_list'] = ItemPrices.objects.all()
       # context['academic_ll'] = AcademicYearSemester.objects.all()
        return context


def add_items(request):
    """Items are added to database"""
    try:
        name = request.POST['item_name']
        description = request.POST['item_description']

        item_obj = Item.objects.create(
            name=name,
            description=description
        )

        data = {
            'success_stat': 1,
            'id': item_obj.id,
            'name': item_obj.name,
            'description': item_obj.description
        }
        return JsonResponse(data)
    except Exception as e:
        logger.exception(e)
        data = {
            'success_stat': 0,
            'error_message': 'Unable to process request',
        }
        return JsonResponse(data)


def add_prices(request, pk):
    """Item prices are added to database"""
    try:
        price = request.POST['price']
        supplier_id = request.POST['supplier']

        item_object = Item.objects.get(pk=pk)
        supplier_object = Supplier.objects.get(pk=supplier_id)

        item_price = ItemPrices.objects.create(
            supplier=supplier_object,
            item=item_object,
            price=price
        )

        data = {
            'success_stat': 1,
            'id': item_price.id,
            'price': item_price.price,
            'supplier_id': item_price.supplier.id
        }
        return JsonResponse(data)
    except MultiValueDictKeyError as mk:
        logger.exception(mk)
        data = {
            'success_stat': 0,
            'error_message': 'Unable to process request',
        }
        return JsonResponse(data)


class CreateItemPrices(generic.DetailView):
    """View item prices page"""
    model = Item
    template_name = 'accounting/item-prices.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['supplier_list'] = Supplier.objects.all()
        return context


class ViewPurchaseOrders(generic.ListView):
    """"View a list of purchase orders created by account staff"""
    model = Orders
    template_name = 'accounting/purchase-orders.html'


def view_order_request(request, pk):
    requestorders = RequestOrders.objects.get(pk=pk)
    price_list = ItemPrices.objects.filter(item=requestorders.item)
    print(price_list)
    context = {
        'price_list': price_list,
        'requestorders': requestorders
    }
    return render(request, 'accounting/purchase-order-create.html', context)


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
