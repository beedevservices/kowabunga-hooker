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

def apiAllByCust(request):
    orders = list(Order.objects.all().values())
    users = list(User.objects.all().values())
    categories = list(Category.objects.all().values())
    products = list(Product.objects.all().values())
    profiles = list(Profile.objects.all().values())
    invoices = list(Invoice.objects.all().values())

    ordersByCustomer = {}
    customers = []
    for u in users:
        orders = []
        # print(u['id'])
        for p in profiles:
            if p['user_id'] == u['id']:
                for o in orders:
                    print(o)
                    if o['customer_id'] == u['id']:
                        orders.append(o)
                customer = {'user': u, 'profile': p, 'orders': orders}
        customers.append(customer)
        ordersByCustomer = {'customers': customers}
    context = {
        'ordersByCustomer': ordersByCustomer
    }
    return JsonResponse(context, content_type='application/json')