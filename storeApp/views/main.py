from django.shortcuts import render , redirect , HttpResponseRedirect
from storeApp.models import *

def index(request):
    cart = request.session['cart']
    if not cart:
        request.session['cart'] = {}
    categories = Category.getAllCategories()
    catId = request.GET.get('category')
    if catId:
        products = Product.getAllByCatId(catId)
    else:
        products = Product.getAllProds()
    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'index.html', context)