"""The class for logging to server"""
import logging

from django.shortcuts import render  # , redirect
from django.utils.datastructures import MultiValueDictKeyError
from django.http import JsonResponse
from django.views import generic
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.db.utils import IntegrityError

from orders.serializers import DeliveryLogSerializer, StockSerializer, requestOrdersSerializer
from rest_framework.decorators import api_view

from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from orders.models import Item, OrderStatus, RequestOrders, Site, Stock, Orders
from orders.models import Employee, ItemPrices, Supplier


logger = logging.getLogger(__name__)

#@login_required
class ViewItems(generic.ListView):
    """View a list of saved catalog items."""
    model = Item
    template_name = 'accounting/items-catalog.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['itemprices_list'] = ItemPrices.objects.all()
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
            'success_status': 1,
            'id': item_obj.id,
            'name': item_obj.name,
            'description': item_obj.description
        }
        return JsonResponse(data)
    except Exception as e:
        logger.exception(e)
        data = {
            'success_status': 0,
            'error_message': 'Unable to process request',
        }
        return JsonResponse(data)


def add_prices(request, pk):
    """Item prices are added to database"""
    success_status = 0  # initially success status is set to zero
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
            'id': item_price.id,
            'price': item_price.price,
            'supplier_id': item_price.supplier.id
        }
        success_status = 1
    except MultiValueDictKeyError as mk:
        logger.exception(mk)
        data = {
            'error_message': 'Unable to process request',
        }
    finally:
        data['success_status'] = success_status
        return JsonResponse(data)


class CreateItemPrices(generic.DetailView):
    """View item prices page"""
    model = Item
    template_name = 'accounting/item-prices.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['supplier_list'] = Supplier.objects.all()
        return context


def delete_prices(request, pk):
    """Delete an existing price of a certain supplier"""
    success_status = 0
    try:
        item_price_id = request.GET.get('item_price_id', None)
        ItemPrices.objects.get(pk=item_price_id).delete()
        success_status = 1
        data = {
            'success_message': 'price deleted successfully'
        }
    except:
        data = {
            'error_message': 'Unable to process request'
        }
    finally:
        data['success_status'] = success_status
        return JsonResponse(data)
