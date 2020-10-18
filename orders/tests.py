from django.test import TestCase
from django.urls import reverse
from orders.models import ItemPrices, Item, Supplier, Site, Location, RequestOrders, OrderStatus, Rule1, Rule2
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
    return    Rule2.objects.create(
        price_limit=price_limit,
        rule_code=rule_code
    )         

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
        url = reverse('item_prices_view', args=(10000,))
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
        url = reverse('view_order_request', args=(10000,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)  


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



