from django.shortcuts import render , redirect , HttpResponseRedirect
from storeApp.models import *
from customerApp.models import *
from customerApp.util import *


def cart(request):
    url = '/cart/'
    request.session['url'] = url
    if 'user_id' not in request.session:
        user = False
        url = '/cart/'
        request.session['url'] = url
        return redirect('/logReg/')
    else:
        user = User.objects.get(id=request.session['user_id'])
        cart = request.session['cart']
        ids = list(request.session.get('cart').keys())
        products = Product.objects.filter(id__in=ids)
        print('thecart', cart, 'theprods', products)
        context = {
            'user': user,
            'cart': cart,
            'products': products,
            'url': url,
        }
        return render(request, 'cart.html', context)
    
def thankYou(request):
    if 'user_id' not in request.session:
        user = False
        return redirect('/')
    else:
        user = User.objects.get(id=request.session['user_id'])
        cart = request.session['cart']
        request.session['order_id'] = None
        request.session['cart'] = {}
        custOrder = request.session['invoice']
        order = Order.objects.get(orderNum=custOrder)
        print('order',order.id)
        sendOrderEmail(user, order)
        context = {
            'user': user,
            'cart': cart,
            'custOrder': custOrder,
        }
        return render(request, 'thankyou.html', context)
