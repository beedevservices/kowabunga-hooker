from django.shortcuts import render , redirect , HttpResponseRedirect
from django.contrib import messages
from storeApp.models import *
from customerApp.models import *

def logReg(request):
    url = request.session['url']
    if 'user_id' not in request.session:
        user = False
        cart = request.session['cart']
        context = {
            'user': user,
            'url': url,
            'cart': cart,
        }
        return render(request, 'logReg.html', context)
    else:
        return redirect(url)

def logout(request):
    request.session.clear()
    messages.error(request, 'You have been logged out')
    return redirect('/')