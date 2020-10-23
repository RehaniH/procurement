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

