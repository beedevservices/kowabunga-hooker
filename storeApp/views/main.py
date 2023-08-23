from django.shortcuts import render , redirect , HttpResponseRedirect
from storeApp.models import *

def index(request):
    
    return render(request, 'index.html')