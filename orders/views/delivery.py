"""The class for logging to server"""
import logging

from django.shortcuts import render  # , redirect
from django.utils.datastructures import MultiValueDictKeyError
from django.views.generic import ListView
from django.views.generic import View
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render
# andrew
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from orders.models import DeliveryLog, Item, OrderStatus, RequestOrders, Site, Stock, Orders
from orders.serializers import DeliveryLogSerializer, ItemSerializer, OrderSerializer, StockSerializer, requestOrdersSerializer
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


#REQUEST ORDER
@api_view(['GET', 'POST', 'DELETE'])
def requestOrder_list(request):
    if request.method == 'GET':
        requestOrders=RequestOrders.objects.all()
        requestOrder_Serializer=requestOrdersSerializer(requestOrders,many=True)
        return JsonResponse(requestOrder_Serializer.data,safe=False)
        
    elif request.method == 'POST':
        reqorder_data = JSONParser().parse(request)
        print(reqorder_data)
        itemid = reqorder_data['item']
        print(itemid)
        quantityy=reqorder_data['quantity']
        print(quantityy)
        expected_datee=reqorder_data['expected_date']
        commentt=reqorder_data['comment']
        qnty_typee=reqorder_data['quantity_type']
        print(qnty_typee)
        itemm = Item.objects.get(name=itemid)
        print(itemm)
        statusobj=OrderStatus.objects.get(status__iexact='pending')
        print(statusobj)
        siteobj=Site.objects.get(name__iexact='galle')
        obj=RequestOrders.objects.create(
                item=itemm,
                quantity=quantityy,
                comment=commentt,
                status=statusobj,
                site=siteobj,
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
        quantityy=reqorder_data['quantity']
        print(quantityy)
        expected_datee=reqorder_data['expected_date']
        commentt=reqorder_data['comment']
        obj=RequestOrders.objects.get(id=pk)
        obj.expected_date=expected_datee
        obj.quantity=quantityy
        obj.comment=commentt

        
        obj.save()
       

        request_serializer = requestOrdersSerializer(requestOrder, data=reqorder_data) 
        if request_serializer.is_valid(): 
            # request_serializer.save() 
            return JsonResponse(request_serializer.data) 
        return JsonResponse(request_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
 
    elif request.method == 'DELETE': 
        requestOrder.delete() 
        return JsonResponse({'message': 'request order was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    

#DELIVERY LOG
@api_view(['GET', 'POST', 'DELETE'])
def DeliveryLog_list(request):
    if request.method == 'GET':
        Delivery_Log=DeliveryLog.objects.all()
        DeliveryLog_Serializer=DeliveryLogSerializer(Delivery_Log,many=True)
        return JsonResponse(DeliveryLog_Serializer.data,safe=False)

    elif request.method == 'POST':
        DeliveryLog_data = JSONParser().parse(request)
        print(DeliveryLog_data['purchased_orders'])
        id = DeliveryLog_data['purchased_orders']
        id_val=Orders.objects.get(pk=id)
        print(id_val)
        order = Orders.objects.values_list('item',flat=True).get(pk=id)
        print(order,"ss")
        item1=Item.objects.get(pk=order)
        print(item1)
        stock = Stock.objects.get(item_id=order)
        
        stock.quantity += DeliveryLog_data['quantity']
        orderobj=Orders.objects.get(pk=id)
        orderobj.remaining_quantity-= DeliveryLog_data['quantity']
        if(orderobj.remaining_quantity<=0):
            orderobj.status=OrderStatus.objects.get(status='completed')
        orderobj.save()

        stock.save()


        print(stock)
        obj=DeliveryLog.objects.create(
                item=item1,
                purchased_orders=id_val,
                quantity=DeliveryLog_data['quantity'],
                date=DeliveryLog_data['date']

            )


        Dellog_serializer = DeliveryLogSerializer(data=DeliveryLog_data)
        #order id -> order record-> item(4)=stock.item(4)
        if Dellog_serializer.is_valid():
            # Dellog_serializer.save()
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
        Deliverylog_serializer = DeliveryLogSerializer(Delivery_log, data=DeliveryLog_data) 
        if Deliverylog_serializer.is_valid(): 
            Deliverylog_serializer.save() 
            return JsonResponse(Deliverylog_serializer.data) 
        return JsonResponse(Deliverylog_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
 
    elif request.method == 'DELETE': 
        Delivery_log.delete() 
        return JsonResponse({'message': 'Deliverylog was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

#Stock
@api_view(['GET', 'POST', 'DELETE'])
def Stock_list(request):
    if request.method == 'GET':
        Stocks=Stock.objects.all()
        Stock_Serializer=StockSerializer(Stocks,many=True)
        return JsonResponse(Stock_Serializer.data,safe=False)

    elif request.method == 'POST':
        stock_data = JSONParser().parse(request)
        print(stock_data)
        itemid = stock_data['item']
        print(itemid)
        quantityy=stock_data['quantity']
        print(quantityy)
        quantity_typee=stock_data['quantity_type']
        # reorder_levell=stock_data['reorder_level']
        itemm = Item.objects.get(name=itemid)
        print(itemm)
        siteobj=Site.objects.get(name__iexact='galle')
        

        obj=Stock.objects.create(
                item=itemm,
                quantity=quantityy,
                quantity_type=quantity_typee,
                # reorder_level=reorder_levell,
                site=siteobj,
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
        qnty=Stock_data['quantity']
        print(qnty)
        obj1=Stock.objects.get(id=pk)
        obj1.quantity=qnty
        obj1.save()      
        
        # print(Stock_data['item'])
        Item_id=obj1.item
        orderobj=Item.objects.get(name=Item_id)
        statusobj=OrderStatus.objects.get(status__iexact='reorder item')
        
        print(orderobj)
        if(qnty<=Stocks.reorder_level):
            obj=RequestOrders.objects.create(
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

#Stock
@api_view(['GET', 'POST', 'DELETE'])
def Order_list(request):
    if request.method == 'GET':
        Stocks=Orders.objects.all()
        # for x in Stocks:
        #     Item1=x.item
        #     order_id=Orders.objects.get(pk=x.id)
        #     print(Item1)
        #     obj=DeliveryLog.objects.create(
        #         item=Item1,
        #         purchased_orders=order_id
    
        #      )
        
        
        
        Order_Serializer=OrderSerializer(Stocks,many=True)
        return JsonResponse(Order_Serializer.data,safe=False)

@api_view(['GET', 'PUT', 'DELETE'])
def Order_detail(request, pk):
    try: 
        orders = Orders.objects.get(pk=pk) 
    except Stock.DoesNotExist: 
        return JsonResponse({'message': 'The stock does not exist'}, status=status.HTTP_404_NOT_FOUND) 
    
    if request.method == 'GET': 
        Order_serializer = OrderSerializer(orders) 
        return JsonResponse(Order_serializer.data) 
 
    elif request.method == 'PUT': 
        Order_data = JSONParser().parse(request) 
        print(Order_data)
        quantity1=Order_data['quantity']
        statusobj=OrderStatus.objects.get(abbv__iexact='RQEDI')
        obj2=Orders.objects.get(id=pk)
        obj2.quantity=quantity1
        obj2.status=statusobj
        obj2.save()

        Order_serializer = OrderSerializer(orders, data=Order_data) 
        if Order_serializer.is_valid(): 
            # Stock_serializer.save() 
            return JsonResponse(Order_serializer.data) 
        return JsonResponse(Order_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
 
    elif request.method == 'DELETE':
        statusobj=OrderStatus.objects.get(abbv__iexact='RQDEL')
        obj2=Orders.objects.get(id=pk)
        obj2.status=statusobj
        obj2.save() 
        
        return JsonResponse({'message': 'Stock was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
 
def Item_list(request):
    # if(request.method)=='GET':
        name=Item.objects.values_list('name',flat=True)
        Item2=list(name)
        print(Item2)
        # Item_Serializer=ItemSerializer(name,many=True)
        # return JsonResponse(Item_Serializer.data,safe=False)
        return JsonResponse(Item2,safe=False) 

def Reorder_level(request,pk):
    try: 
        orders = Stock.objects.get(pk=pk) 
    except Stock.DoesNotExist: 
        return JsonResponse({'message': 'The stock does not exist'}, status=status.HTTP_404_NOT_FOUND) 
    
    if request.method == 'PUT': 
        reorder_level_data = JSONParser().parse(request) 
        print(reorder_level_data)
        re_order=reorder_level_data['reorder_level']
        obj3=Stock.objects.get(id=pk)
        obj3.reorder_level=re_order
        obj3.save()

        Stock_serializer = StockSerializer(orders, data=reorder_level_data) 
        if Stock_serializer.is_valid(): 
            # Stock_serializer.save() 
            return JsonResponse(Stock_serializer.data) 
        return JsonResponse(Stock_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
 