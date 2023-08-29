from django.shortcuts import render , redirect , HttpResponseRedirect
from storeApp.models import *
from customerApp.models import *
from customerApp.util import *

def index(request):
    cart = request.session.get('cart')
    url = '/'
    request.session['url'] = url
    # print(cart)
    if not cart:
        request.session['cart'] = {}
    categories = Category.getAllCategories()    
    products = Product.getAllProds()
    if 'user_id' not in request.session:
        user = False
        categories = categories.filter(adultOnly=False)
        products = products.filter(adultOnly=False)
    if 'user_id' in request.session:
        user = User.objects.get(id=request.session['user_id'])
        isAdult = checkAge(user)
        print(isAdult)
        if isAdult == False:
            categories = categories.filter(adultOnly=False)
            products = products.filter(adultOnly=False)
    if 'filtered' in request.session:
        theID = request.session['filtered']
        if theID != 0:
        # categories = categories.filter(id=theID)
            products = products.filter(category_id=theID)
    context = {
        'categories': categories,
        'products': products,
        'cart': cart,
        'user': user,
        'url': url,
    }
    # print(context)
    # print(cart)
    return render(request, 'index.html', context)

def catFilter(request, id):
    request.session['filtered'] = id
    return redirect('/')


def viewProduct(request, prod_name):
    url = '/cart/'
    request.session['url'] = url
    if 'user_id' not in request.session:
        user = False
    else:
        user = User.objects.get(id=request.session['user_id'])
    cart = request.session['cart']
    product = Product.objects.get(name=prod_name)
    categories = Category.objects.all().values()
    theImages = ProductImages.objects.filter(prod_id=product.id)
    images = []
    images.append(product)
    for i in theImages:
        images.append(i)
    print(images)
    context = {
        'user': user,
        'cart': cart,
        'product': product,
        'categories': categories,
        'images': images,
    }
    return render(request, 'viewProduct.html', context)

def addToCart(request):
    product = request.POST.get('prod_id')
    remove = request.POST.get('remove')
    add = request.POST.get('add')
    cart = request.session.get('cart')
    thePrice = request.POST.get('price')
    item = Product.objects.get(id=request.POST.get('prod_id'))
    print('product',product, 'cart', cart, 'item', item, 'remove', remove, 'add', add, 'price', thePrice)
    if add:
        plus = cart.get(str(item.id))['quantity']
        price = int(cart.get(str(item.id))['price'])
        total = int(cart.get(str(item.id))['total'])
        plus = plus+1
        total = price * plus
        cart[str(product)]['quantity'] = plus
        cart[str(product)]['total'] = total
        print('add more to the cart', cart)
    elif remove:
        min = cart.get(str(item.id))['quantity']
        price = int(cart.get(str(item.id))['price'])
        total = int(cart.get(str(item.id))['total'])
        if min <= 1:
            cart.pop(product)
        else:
            min = min-1
            total = price * min
            cart[str(product)]['quantity'] = min
            cart[str(product)]['total'] = total
            print('remove from cart', cart)
    else:
        if cart == {}:
            print('empty cart', cart)
            item = cart.get(str(item.id), {})
            quantity = item.get('quantity', 0)
            price = (item.get('price', thePrice))
            total = item.get('total', 0)
            item['quantity'] = quantity+1
            item['price'] = price
            total = item['price']
            item['total'] = total
            cart[str(product)] = item
            print('new cart', cart)
        else:
            # print('the cart', cart)
            item = cart.get(str(item.id), {})
            quantity = item.get('quantity', 0)
            price = item.get('price', thePrice)
            total = item.get('total', 0)
            item['quantity'] = quantity+1
            item['price'] = price
            total = item['price']
            item['total'] = total
            cart[str(product)] = item
            print('new cart', cart)
    # if cart:
    #     pass
    # else:
    #     cart = {}
    #     cart[str{prod_id}] = {
    #         'quantity': 1,
    #         'price': 
    #     }
    # if cart:
    #     quantity = cart.get(product)
    #     print(cart, quantity)
    #     if quantity:
    #         if remove:
    #             if quantity <= 1:
    #                 cart.pop(product)
    #             else:
    #                 cart[product] = quantity-1
    #         else:
    #             cart[product]  = quantity+1
    #     else:
    #         cart[product] = 1
    # else:
    #     cart = {}
    #     cart[product] = 1
    request.session['cart'] = cart
    print(request.session['cart'])
    return redirect('/')