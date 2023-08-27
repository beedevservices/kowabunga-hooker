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

def apiAllData(request):
    theOrders = list(Order.objects.all().values())
    users = list(User.objects.all().values())
    categories = list(Category.objects.all().values())
    theProducts = list(Product.objects.all().values())
    profiles = list(Profile.objects.all().values())
    invoices = list(Invoice.objects.all().values())
    theItems = list(OrderItem.objects.all().values())
    context = {
        'theOrders': theOrders,
        'users': users,
        'categories': categories,
        'theProducts': theProducts,
        'profiles': profiles,
        'invoices': invoices,
        'theItems': theItems,
    }
    return JsonResponse(context, content_type='application/json')

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

def apiOneCustomer(request, user_id):
    users = list(User.objects.all().values())
    profiles = list(Profile.objects.all().values())
    customer = {}
    for u in users:
        if u['id'] == user_id:
            for p in profiles:
                if p['user_id'] == user_id:
                    customer = {'user': u, 'profile': p}
    return JsonResponse(customer, content_type='application/json')

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

def apiOneProduct(request, prod_id):
    categories = list(Category.objects.all().values())
    theProducts = list(Product.objects.all().values())
    product = {}
    for prod in theProducts:
        if prod['id'] == prod_id:
            for cat in categories:
                if cat['id'] == prod['category_id']:
                    product = {'product': prod, 'category': cat}
    return JsonResponse(product, content_type='application/json')

def apiAllOrderNumbers(request):
    theOrders = list(Order.objects.all().values())
    orderNumbers = []
    for o in theOrders:
        aOrder = o['orderNum']
        if aOrder not in orderNumbers:
            orderNumbers.append(aOrder)
    context = {
        'orderNumbers': orderNumbers
    }
    return JsonResponse(context,content_type='application/json')

def apiOneOrderNumber(request, orderNum):
    theOrders = list(Order.objects.all().values())
    orders = []
    for o in theOrders:
        if o['orderNum'] == orderNum:
            order = {'order': o}
            orders.append(order)
    context = {
        'orders': orders,
    }
    return JsonResponse(context,content_type='application/json')

def apiAllInvoiceNumbers(request):
    theInvoices = list(Invoice.objects.all().values())
    invoiceNumbers = []
    for i in theInvoices:
        oneI = i['orderNum']
        if oneI not in invoiceNumbers:
            invoiceNumbers.append(oneI)
    context = {
        'invoiceNumbers': invoiceNumbers,
    }
    return JsonResponse(context,content_type='application/json')

def apiOneInvoiceNumber(request, orderNum):
    theInvoices = list(Order.objects.all().values())
    invoice = {}
    for i in theInvoices:
        if i['orderNum'] == orderNum:
            invoice = {'invoice': i}
    return JsonResponse(invoice, content_type='application/json')

def apiAllOrderItems(request):
    theItems = list(OrderItem.objects.all().values())
    return JsonResponse(theItems, content_type='application/json')

# theOrders = list(Order.objects.all().values())
# users = list(User.objects.all().values())
# categories = list(Category.objects.all().values())
# theProducts = list(Product.objects.all().values())
# profiles = list(Profile.objects.all().values())
# invoices = list(Invoice.objects.all().values())