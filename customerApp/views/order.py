from django.shortcuts import render , redirect , HttpResponseRedirect
from django.contrib import messages
from storeApp.models import *
from customerApp.models import *
from customerApp.util import *
from django.views import View
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

def placeOrder(request):
    url = request.session['url']
    if 'user_id' not in request.session:
        return redirect('/logReg/')
    customer = User.objects.get(id=request.session['user_id'])
    if not customer.profile.address01:
        return redirect('/profile/')
    orderNumber = Order.objects.validate()
    newOrder = Order.objects.create(
        orderNum=orderNumber,
        customer=customer
    )
    print('order instance created', newOrder.id)
    orderTotal = 0
    itemCount = 0
    TBD = False
    cart = request.session['cart']
    print('place order cart',cart)
    for item in cart:
        quantity = 0
        total = 0
        print('item in placeorderloop', item, 'quantity', cart.get(item)['quantity'], 'total', cart.get(item)['total'])
        if cart.get(item)['total'] == 'TBD':
            quantity = cart.get(item)['quantity']
            total = cart.get(item)['total']
            itemCount += quantity
            TBD = True
            total = TBD
        else:
            quantity = cart.get(item)['quantity']
            total = int(cart.get(item)['total'])
            itemCount += quantity
            orderTotal += total
        newItem = OrderItem.objects.create(
            orderNum = Order.objects.get(id=newOrder.id),
            product = Product.objects.get(id=item),
            quantity = quantity,
            total = total,
        )
        print(newItem)
    if TBD == True:
        orderTotal = f'{orderTotal} + Custom Items'
    else:
        orderTotal = str(orderTotal)
    toUpdate = Order.objects.get(id=newOrder.id)
    toUpdate.itemCount = itemCount
    toUpdate.orderTotal = orderTotal
    toUpdate.save()
    # request.session['cart'] = {}
    request.session['order_id'] = newOrder.id
    # sendOrderEmail(customer, updatedOrder)
    # return redirect('/thankyou/')
    return redirect('/customer/generateInvoice/')
    # return redirect('/customer/confirm/')

  
def generateInvoice(request):
    buffer = io.BytesIO()
    # Create a PDF object
    p = canvas.Canvas(buffer, pagesize=letter)
    # Add content to the PDF
    p.drawString(700, 750, "Hello, World!")

    # Close the PDF object
    p.save()

    # Move the buffer's position back to the beginning
    buffer.seek(0)

    # Set the response content type
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="example.pdf"'
    response.write(buffer.read())

    return response
    

def confirmOrder(request):
    theOrder = Order.objects.get(id=request.session['order_id'])
    user = User.objects.get(id=request.session['user_id'])
    cart = request.session['cart']
    context = {
        'theOrder': theOrder,
        'user': user,
        'cart': cart,
    }
    return render(request, 'confirmOrder.html', context)