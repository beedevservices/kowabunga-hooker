from django.shortcuts import render , redirect , HttpResponseRedirect
from storeApp.models import *
from customerApp.models import *
from customerApp.util import *


def custOrder(request):
    url = request.session['url']
    cart = request.session['cart']
    ids = list(request.session.get('cart').keys())
    products = Product.objects.filter(id__in=ids)
    customer = request.session.get('user_id')
    profile = Profile.objects.get(user=request.session['user_id'])
    address = profile.address()
    phone = profile.tel()
    for prod in products:
        order = Order(customer=User(id=customer),
                    product=prod,
                    price=prod.price,
                    address=address,
                    phone=phone,
                    quantity=cart.get(str(prod.id)))
        order.save()
        request.session['cart'] = {}
    return redirect(url)