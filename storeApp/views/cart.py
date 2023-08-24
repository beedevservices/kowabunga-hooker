from django.shortcuts import render , redirect , HttpResponseRedirect
from storeApp.models import *
from customerApp.models import *


def cart(request):
    if 'user_id' not in request.session:
        user = False
        url = '/cart/'
        request.session['url'] = url
        return redirect('/logReg/')