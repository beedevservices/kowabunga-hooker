from django.shortcuts import render , redirect , HttpResponseRedirect
from django.contrib import messages
from storeApp.models import *
from customerApp.models import *
from customerApp.util import *
from django.views import View
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import io
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import os

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
    request.session['order_id'] = newOrder.id
    print('order', request.session['order_id'], 'user', request.session['user_id'])
    # return redirect(f'/customer/generateInvoice/{newOrder.id}/')
    return redirect('/customer/confirm/')

def generateInvoice(user_id, order_id):
    products = Product.objects.all().values()
    order = Order.objects.get(id=order_id)
    user = User.objects.get(id=order.customer_id)
    theOrderItems = OrderItem.objects.filter(orderNum_id=order.id)
    company = {
        'name': 'Kowabunga Hooker',
        'email': 'orders@kowabunga-hooker.com'
    }
    orderItems = [
        ['Item Name', 'Price', 'Quantity', 'Total']
    ]
    for i in theOrderItems:
        for prod in products:
            if(i.product_id == prod['id']):
                name = prod['name']
                quantity = i.quantity
                if(prod['price'] == None):
                    price = 'TBD'
                else:
                    price = prod['price']
                if(i.total == 'True'):
                    total = 'TBD'
                else: 
                    total = i.total
                orderItems.append([name, price, quantity, total])
    rowCount = []
    for i in orderItems:
        rowCount.append(30)
    print(rowCount)
   

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.drawString(60, 750, f"{company['name']}")
    p.drawString(60, 730, f"{company['email']}")
    p.drawString(340, 670, f"{user.firstName} {user.lastName}")
    p.drawString(340, 650, f"{user.profile.address01} {user.profile.address02}")
    p.drawString(340, 630, f"{user.profile.city}, {user.profile.state} {user.profile.zip}")
    p.drawString(340, 610, f"Order #:{order.orderNum}")
    p.drawString(340, 590, f"{user.profile.phone}")
    orderItemsTable = Table(orderItems, colWidths=[120, 120, 120, 120], rowHeights=rowCount)
    orderItemsTable.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.seagreen),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.antiquewhite),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.antiquewhite),
        ('GRID', (0, 0), (-1, -1), 1, colors.darkslateblue),
    ]))
    w, h = orderItemsTable.wrapOn(p, 0, 0)
    orderItemsTable.drawOn(p, 60, 550 - h)
    p.drawString(60, 310, f'Order Total: ${order.orderTotal}')
    p.drawString(60, 290, f'Total Item Count: {order.itemCount}')
    p.drawString(60, 270, f'Thank you {user.firstName}, for placing order # {order.orderNum}.')
    p.drawString(60, 250, f'I will reach out as soon as possible to get and give further details on your order.')
    p.drawString(60, 30, f'orders@kowabunga-hooker.com')
    p.save()
    buffer.seek(0)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="invoice.pdf"'
    response.write(buffer.read())

    return response
    
def confirmOrder(request):
    theOrder = Order.objects.get(id=request.session['order_id'])
    user = User.objects.get(id=request.session['user_id'])
    cart = request.session['order_id']
    context = {
        'theOrder': theOrder,
        'user': user,
        'cart': cart,
    }
    return render(request, 'confirmOrder.html', context)

def saveInvoice(request):
    user = User.objects.get(id=request.session['user_id'])
    order = Order.objects.get(id=request.session['order_id'])
    pdfContent = generateInvoice(user.id, order.id)
    theOrder = Order.objects.get(id=request.session['order_id'])
    cart = request.session['order_id']
    # Save the PDF content using Django's file storage
    pdf_path = os.path.join('invoices', f'{order.orderNum}.pdf')
    pdf_file = ContentFile(pdfContent.getvalue())
    pdf_storage_path = default_storage.save(pdf_path, pdf_file)

    # Create an Invoice instance
    invoice = Invoice.objects.create(
        theCustomer=user,
        cart=order,
        orderDate=datetime.datetime.today(),
        pdf=pdf_storage_path,  # Save the path to the PDF file
    )
    messages.error(request, 'Order Created')
    print('invoice', invoice.id)
    theOrder = f'{theOrder.orderNum}'
    request.session['invoice'] = theOrder
    return redirect('/thankyou/')
