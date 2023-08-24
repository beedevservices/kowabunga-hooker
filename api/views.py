from django.http import JsonResponse, HttpResponse
from django.core.serializers import serialize
from django.shortcuts import render, redirect
from django.contrib import messages
from customerApp.models import *
from storeApp.models import *


status = {
    "API Status": "Running"
}

def apiBase(request):
    return JsonResponse(status, content_type="application.json")

def apiAllCustomers(request):
    users = list(User.objects.all().values())
    profiles = list(Profile.objects.all().values())
    customers = []
    customer = {}
    for u in users:
        for p in profiles:
            if p['user_id'] == u['id']:
                customer = {'user': u, 'profile': p}
        customers.append({'customer': customer})
    context = {
        'customers': customers,
    }
    return JsonResponse(context, content_type='application/json')

def apiAllProducts(request):
    categories = list(Category.objects.all().values())
    theProducts = list(Product.objects.all().values())
    products = []
    product = {}
    for prod in theProducts:
        for cat in categories:
            if cat['id'] == prod['category_id']:
                product = {'product': prod, 'category': cat}
        products.append({'product': product})
    context = {
        'products': products,
    }
    return JsonResponse(context, content_type='application/json')

def apiAllOrders(request):
    theOrders = list(Order.objects.all().values())
    theProducts = list(Product.objects.all().values())
    categories = list(Category.objects.all().values())
    orderNumbers = []
    orders = []
    order = {}
    products = []
    product = {}
    items = []
    item = {}
    for prod in theProducts:
        for cat in categories:
            if cat['id'] == prod['category_id']:
                product = {'product': prod, 'category': cat}
        products.append({'product': product})
    for o in theOrders:
        print(o['orderNumber'])
        aOrder = o['orderNumber']
        if aOrder not in orderNumbers:
            orderNumbers.append(aOrder)
    for o in theOrders:
        for num in orderNumbers:
            if o['orderNumber'] == num:
                print('the o', o, 'the num', num)
                items.append(o['quantity'])
            order = {num: items}
        orders.append(order)
    context = {
        'orders': orders
    }
    return JsonResponse(context,content_type='application/json')
    

def apiAllByCust(request):
    theOrders = list(Order.objects.all().values())
    users = list(User.objects.all().values())
    categories = list(Category.objects.all().values())
    theProducts = list(Product.objects.all().values())
    profiles = list(Profile.objects.all().values())
    invoices = list(Invoice.objects.all().values())
    # print(orders)
    ordersByCustomer = []
    customers = []
    customer = {}
    orders = []
    order = {}
    products = []
    product = {}
    for u in users:
        for p in profiles:
            if p['user_id'] == u['id']:
                customer = {'user': u, 'profile': p}
        customers.append({'customer': customer})
    for prod in products:
        for cat in categories:
            if cat['id'] == prod['category_id']:
                product = {'product': prod, 'category': cat}
        products.append({'product': product})
    ordersByCustomer.append(customers)
        # for prod in products:
        #     if prod['id'] == o['product_id']:
        #         print(prod)
        # for u in users:
        #     if u['id'] == o['customer_id']:
        #         orders.append(o)
        #     for p in profiles:
        #         if p['user_id'] == u['id']:
        # for o in orders:
        #     print('o', o['id'], 'u', u['id'])
        #     if o['customer_id'] == u['id']:
        #         orders.append(o)
        # for p in profiles:
        #     if p['user_id'] == u['id']:
        #         customer = {'user': u, 'profile': p, 'orders': orders}
        # customers.append(customer)
        # ordersByCustomer = {'customers': customers}
    context = {
        'ordersByCustomer': ordersByCustomer
    }
    return JsonResponse(context, content_type='application/json')