from django.shortcuts import render, redirect
from django.contrib import messages
from customerApp.models import *
from storeApp.models import *
from customerApp.util import *

def profile(request):
    if 'user_id' not in request.session:
        messages.error(request, "you need to be logged in to view this page")
        return redirect('/logReg/')
    else:
        user = User.objects.get(id=request.session['user_id'])
        cart = request.session['cart']
        context = {
            'user': user,
            'cart': cart,
        }
        return render(request, 'profile.html', context)
    
def updateProfile(request):
    toUpdate = User.objects.get(user=request.session['user_id'])
    toUpdate.profile.address01 = request.POST['address01']
    toUpdate.profile.address02 = request.POST['address02']
    toUpdate.profile.city = request.POST['city']
    toUpdate.profile.state = request.POST['state']
    toUpdate.profile.zip = request.POST['zip']
    toUpdate.profile.phone = request.POST['phone']
    toUpdate.save()
    messages.error(request, 'Updated address')
    return redirect('/customer/profile/')