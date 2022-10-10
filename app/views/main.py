from django.shortcuts import render, redirect
from django.contrib import messages
from app.models import *
from app.general import *


def index(request):
    return render(request, 'index.html')

def store(request):
    return render(request, 'store.html')