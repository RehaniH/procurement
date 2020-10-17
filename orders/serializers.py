from rest_framework import serializers 
from orders.models import DeliveryLog, Item, RequestOrders, Stock

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
            'status'
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
            'quantity',
            'qnty_type',
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