from django.test import TestCase
from django.urls import reverse
import orders.views as views
from orders.models import (
    ItemPrices, Item, Supplier, Site, Location, RequestOrders, OrderStatus, Rule1, Rule2, Orders, DeliveryLog, Stock)
# Create your tests here.


def create_item(name, description):
    """create an item object"""
    return Item.objects.create(
        name=name,
        description=description
    )


def create_item_price(supplier, item, price):
    """create a site object"""
    return ItemPrices.objects.create(
        item=item,
        supplier=supplier,
        price=price
    )


def create_site(name, location, contact_number, budget):
    """create a site object"""
    return Site.objects.create(
        name=name,
        location=location,
        contact_number=contact_number,
        #budget=budget
    )


def create_location(address_line1, address_line2, address_line3, city, postal_code):
    """create a location object"""
    return Location.objects.create(
        address_line1=address_line1,
        address_line2=address_line2,
        address_line3=address_line3,
        city=city,
        postal_code=postal_code
    )


def create_supplier(contact_number, company_address, company_name, email):
    """create a supplier object"""
    return Supplier.objects.create(
        contact_number=contact_number,
        company_address=company_address,
        company_name=company_name,
        email=email
    )

def create_request_orders(item, quantity, quantity_type, expected_date, status):
    return RequestOrders.objects.create(
        item=item,
        quantity=quantity,
        quantity_type=quantity_type,
        expected_date=expected_date,
        status=status
    )  

def create_order_status(status, abbv):
    return OrderStatus.objects.create(
        status=status,
        abbv=abbv
    ) 

def create_rule1(item, rule_code):
    return    Rule1.objects.create(
        item=item,
        rule_code=rule_code
    )    

def create_rule2(price_limit, rule_code):
    return Rule2.objects.create(
        price_limit=price_limit,
        rule_code=rule_code,
        active_status=True
    )         
def create_orders(item, price, supplier, quantity, quantity_type, request):
    return Orders.objects.create(
        item=item, 
        supplier=supplier, 
        price=price, 
        quantity=quantity, 
        quantity_type=quantity_type, 
        request=request
    )

def create_delivery_log(item, quantity, purchased_orders, date):
    return DeliveryLog.objects.create(
        item=item, 
        quantity=quantity, 
        purchased_orders=purchased_orders,
        date=date
    )

def create_stock(item, quantity, quantity_type, site, reorder_level):
    return Stock.objects.create(
        item=item ,
        quantity=quantity, 
        quantity_type=quantity_type, 
        site=site, 
        reorder_level=reorder_level
        
        )    

#Rehani
class ItemDetailViewTests(TestCase):

    def test_existing_item(self):
        """
        The detail view of an existing item
        returns a 200 success.
        """
        item = create_item('Sand', 'fine sand')
        url = reverse('item_prices_view', args=(item.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, item)
        
    def test_non_existing_item(self):
        """
        The detail view of an item with non existing id
        returns a 404 not found.
        """
        non_existing_id = 10000
        url = reverse('item_prices_view', args=(non_existing_id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

class ViewRequestsTests(TestCase):
    def test_existing_requests_sites(self):
        """
        The list view of an order requests available under each site
        returns a query set.
        """
        location = create_location(
             '320', 'Jathissa Mawatha', 'Negambo Road', 'Mabola', '90122')
        site = create_site( 'Sumathi Place',location, '078912290', 1900000)     
        
        url = reverse('list_order_requests')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['sites_list'], ['<Site: Sumathi Place>'])
        
    def test_non_existing_requests_sites(self):
        """
        The list view of an order requests available under each site
        returns an empty set.
        """
        url = reverse('list_order_requests')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['sites_list'], [])

class AddItemPricesTest(TestCase):
    def test_add_item_price(self):
        location = create_location(
            '320', 'Jathissa Mawatha', 'Negambo Road', 'wattala', '90122')
        supplier = create_supplier(
            '0771290112', location, 'Maha Traders', 'maha@gmail.com')
        item = create_item('Cement', 'fine cement for longer lifetime')
        url = reverse('item_prices_add', args=(item.id,))

        data = {
            'price': 300,
            'supplier': supplier.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)#success response code

    def test_add_item_price_failure(self):
        non_existing_id = 1000000
        item = create_item('Cement', 'fine cement for longer lifetime')
        url = reverse('item_prices_add', args=(item.id,))

        data = {
            'price': 300,
            'supplier': non_existing_id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.data.success_status, 0)#internal server error response code



class ViewOrderRequestDetailViewTests(TestCase):

    def test_existing_order_request(self):
        """
        The detail view of an existing order request
        returns a 200 success.
        """
        item = create_item('Sand', 'fine sand')
        status = create_order_status('Pending', 'PEND')
        order_request = create_request_orders(item, 5, 'kg', '2020-10-18', status)
        url = reverse('view_order_request', args=(order_request.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, response.context['requestorders'])
        
    def test_non_existin_order_request(self):
        """
        The detail view of an order request with non existing id
        returns a 404 not found.
        """
        non_existing_id = 10000
        url = reverse('view_order_request', args=(non_existing_id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)  

#Shane
class   ViewRulesTests(TestCase):
    def test_existing_rules(self):
        """
        The list view of an rules available 
        returns a query set.
        """
        item = create_item('Rocks', 'hardened bulks of rocks')
        create_rule1(item, 'CODE')
        rule2 = create_rule2(1000, 'CODE2')
        
        url = reverse('rulelist')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['rule2'], Rule2.objects.all())
        
    def test_non_existing_item(self):
        """
        The list view of an order rules available 
        returns an empty set.
        """
        url = reverse('rulelist')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['rule2'], [])


class TestAddRule1View(TestCase):
    def test_add_rule1(self):
        item = create_item('Rocks', 'hardened bulks of rocks')
        #client = APIClient()
        url = reverse('rule1add')
        data = {
            'rulecode': 'test',
            'itemid': item.id
        }
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, 302)#redirect response code

        def test_add_rule1_failure(self):
            non_existing_id = 1000000
            url = reverse('rule1add')
            data = {
                'rulecode': 'test',
                'itemid': non_existing_id
            }
            response = self.client.get(url, data)
            self.assertEqual(response.status_code, 500)#internal server error response code

class TestAddRule2View(TestCase):
    def test_add_rule2(self):
        rule2 = create_rule2(2000, 'TEST2')
        #client = APIClient()
        url = reverse('rule2add')
        data = {
            'ruleid': rule2.id,
            'priceLimit': 109000
        }
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, 302)#redirect response code

    def test_add_rule2_failure(self):
        non_existing_id = 1000000
        url = reverse('rule2add')
        data = {
            'priceLimit': 109000,
            'ruleid': non_existing_id
        }
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, 500)#internal server error response code

#Andrew
class TestAddRequestView(TestCase):
    def test_add_order_request(self):
        item = create_item('Rocks', 'hardened bulks of rocks')
        url = reverse(views.requestOrder_list)
        data = {
            'item': item.id,
            'quantity':400,
            'expected_date': '2020-09-14',
            'comment': 'Bring on time',
            'quantity_type': 'bulk'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)#created response code

    def test_add_order_request_failure(self):
        non_existing_id = 1000000
        url = reverse(views.requestOrder_list)
        data = {
            'item': non_existing_id,
            'quantity':400,
            'expected_date': '2020-09-14',
            'comment': 'Bring on time',
            'quantity_type': 'bulk'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)#bad request server error response code

class AddDeliveryLogTests(TestCase):
    def test_add_delivery_log(self):
        item = create_item('Rocks', 'hardened bulks of rocks')
        location = create_location(
            '320', 'Jathissa Mawatha', 'Negambo Road', 'ja ela', '90122')
        supplier = create_supplier(
            '0771290112', location, 'KeeySiri Traders', 'keeysiri@gmail.com')
        status = create_order_status('Pending', 'PEND')    
        request = create_request_orders(item, 10, 'Kg', '2020-10-30', status)
        order = create_orders(item, 100, supplier, 10, 'Kg', request)
        url = reverse(views.DeliveryLog_list)
        data = {
            'purchased_orders': order.id,
            'quantity':400,
            'completed': False,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)#created response code

    def test_add_delivery_log_failure(self):
        non_existing_id = 1000000
        url = reverse(views.DeliveryLog_list)
        data = {
            'purchased_orders': non_existing_id,
            'quantity':400,
            'completed': False,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)#bad request server error response code

class ViewDeliveryLogTests(TestCase):
    def test_existing_order_request(self):
        """
        The detail view of an existing delivery log request
        returns a 200 success.
        """
        item = create_item('Sand', 'fine sand')
        status = create_order_status('Pending', 'PEND')
        location = create_location(
            '320', 'Jathissa Mawatha', 'Negambo Road', 'ja ela', '90122')
        supplier = create_supplier(
            '0771290112', location, 'KeeySiri Traders', 'keeysiri@gmail.com')
        status = create_order_status('Pending', 'PEND')    
        order_request = create_request_orders(item, 10, 'Kg', '2020-10-30', status)
        order = create_orders(item, 100, supplier, 10, 'Kg', order_request)
        delivery = create_delivery_log(item, 10, order, '202-10-31')
        url = reverse(views.DeliveryLog_detail, args=(delivery.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
    def test_non_existin_order_request(self):
        """
        The detail view of an delivery log with non existing id
        returns a 404 not found.
        """
        non_existing_id = 10000
        url = reverse(views.DeliveryLog_detail, args=(non_existing_id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)  

#Ranul
class ListStockTests(TestCase):
    def test_get_stock_list(self):
        item = create_item('Cement', 'fine sand')
        location = create_location(
            '320', 'Jathissa Mawatha', 'Negambo Road', 'wattala', '90122')
        site = create_site('name', location, '902101212', 10000000)
        create_stock(item, 10, 'Kg', site, 20)

        url = reverse(views.Stock_list)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['Stocks'], ['<Stocks: Stocks object (1)>'])

    def test_get_stock_list_failure(self):
        url = reverse(views.Stock_list)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['sites_list'], [])


class StockDetailViewTests(TestCase):

    def test_existing_stock(self):
        """
        The detail view of an existing stock
        returns a 200 success.
        """
        item = create_item('Blocks', 'fine blocks')
        location = create_location(
            '320', 'Horana Mawatha', 'Nayakkanda Road', 'welisara', '90123')
        site = create_site('name', location, '902101212', 10000000)
        stock = create_stock(item, 10, 'Kg', site, 20)

        url = reverse(views.Stock_detail, args=(stock.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, stock)
        
    def test_non_existing_stock(self):
        """
        The detail view of an stock with non existing id
        returns a 400 bad request.
        """
        non_existing_id = 10000
        url = reverse(views.Stock_detail, args=(non_existing_id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)     

class ItemsAddTests(TestCase):
    #add_items    
    def test_add_item(self):
        url = reverse('add_items')
        data = {
            'item_name': 'test',
            'item_description': 'down'
        }
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, 200)#redirect response code

        def test_add_item_failure(self):
            url = reverse('add_items')
            data = {
                'item_description': ''
            }
            response = self.client.get(url, data)
            self.assertEqual(response.status_code, 500)#internal server error response code
       

    







