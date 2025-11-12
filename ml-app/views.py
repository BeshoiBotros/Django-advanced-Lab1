
from django.http import HttpResponse
from django.db import connections
import time
import cProfile
import pstats
import io
from django.db.models import Q, F
from .models import *
# Create your views here.

def order_list(request):
    
  
    
    # orders = Order.objects.all()
    # result = []
    
    # for order in orders:
    #     customer_name = order.customer.companyName
    #     result.append(f"Customer: {customer_name}----")
    
    
      # Using select_related
    orders = Order.objects.all().select_related('customer')
    
    
    
    
    return HttpResponse(orders)
        
        
def prefetch_order_list(request):
    
    # orders = Order.objects.all()

    # for order in orders:
        
    #     _ = [p.productName for p in order.products.all()]
    
    
    
    #using prefetch_related
    
    orders_prefetch = Order.objects.prefetch_related('products').all()
    
    for order in orders_prefetch:
        # Accessing products does NOT trigger extra queries now
        _ = [p.productName for p in order.products.all()]
    
    
    return HttpResponse(orders_prefetch)


def test_q(request):

    orders = Order.objects.filter(Q(customer__companyName="Alfreds Futterkiste") | Q(shipper__id=1))
    
    return HttpResponse(orders)


def test_f(request):
  
    Product.objects.update(unitPrice=F('unitPrice') + 10)
    
    products = Order.objects.all()
    return HttpResponse(products)



def test_only_defer(request):
    customers_only = Customer.objects.only('companyName')

    customers_defer = Customer.objects.defer('contactTitle')

    return HttpResponse(f"Only: {list(customers_only)}\nDefer: {list(customers_defer)}")


def test_values(request):
    employees_dict = Employee.objects.values('id', 'employeeName', 'title')
    
    return HttpResponse(list(employees_dict))

def test_values_list(request):
    employees_tuple = Employee.objects.values_list('id', 'employeeName', 'title')
    
    return HttpResponse(list(employees_tuple))



def test_index_performance(request):
    
    start_indexed = time.time()
    indexed_customers = Customer.objects.filter(city__icontains="New")[:1000]
    end_indexed = time.time()
    indexed_time = end_indexed - start_indexed

    
    start_non_indexed = time.time()
    non_indexed_customers = Customer.objects.filter(contactTitle__icontains="Manager")[:1000]
    end_non_indexed = time.time()
    non_indexed_time = end_non_indexed - start_non_indexed

    return HttpResponse(
        f"Indexed (city) query time: {indexed_time:.6f} seconds\n"
        f"Non-indexed (contactTitle) query time: {non_indexed_time:.6f} seconds"
    )
    
def test_conn_max_age(request):
   
    default_conn = connections['default']
    old_max_age = default_conn.settings_dict.get('CONN_MAX_AGE', None)

    default_conn.settings_dict['CONN_MAX_AGE'] = 60  

    return HttpResponse(f"Old max_age: {old_max_age}, New max_age: {default_conn.settings_dict['CONN_MAX_AGE']}")

def profile_index_performance(request):
    pr = cProfile.Profile()
    pr.enable

    indexed_customers = Customer.objects.filter(city__icontains="New")
    non_indexed_customers = Customer.objects.filter(contactTitle__icontains="Manager")

    pr.disable()

    s = io.StringIO()
    
    return HttpResponse(s.getvalue())
