from rest_framework import serializers 
from orders.models import DeliveryLog, Item, Orders, RequestOrders, Stock

class requestOrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model=RequestOrders
        fields=(
            'id',
            'item',
            'quantity',
            'expected_date',
            'comment',
            'site',
            'status',
            'quantity_type'
        )
        depth = 1

class DeliveryLogSerializer(serializers.ModelSerializer):
    # dele = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all(),source='item', write_only=True)
    class Meta:
        model=DeliveryLog
        fields=(
            'id',
            'item',
            'purchased_orders',
            'date',
            'quantity'
            
            # 'dele'
            
        )
        depth = 1

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model=Stock
        fields=(
            'id',
            'item',
            'quantity',
            'site',
            'quantity_type',
            'reorder_level'
        )
        depth = 1

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Orders
        fields=(
            'id',
            'item',
            'quantity',
            'remaining_quantity',
            'quantity_type',
            'price',
            'supplier',
            'site',
            'status',
            'approved_by',
            'delivery_date',
            'active',
            'request'
        )
        depth = 1

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=Item
        fields=(
            'id',
            'name'
            
        )
        depth = 1
