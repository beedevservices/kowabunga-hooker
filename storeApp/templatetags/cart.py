from django import template

register = template.Library()


@register.filter(name='inTheCart')
def inTheCart(prod, cart):
    print(cart)
    # return str(prod.id) in cart.keys()
    keys = cart.keys()
    # print('inTheCart:', keys, prod)
    for id in keys:
        if int(id) == prod:
            # print('True')
            return True
    return False
    

@register.filter(name='prodQuantity')
def prodQuantity(prod, cart):
    # print('what is cart', cart)
    keys = cart.keys()
    # print('what is keys',keys)
    for row in keys:
        if int(row) == prod:
            # print('quantity filter', cart.get(row)['quantity'])
            return cart.get(row)['quantity']
    return 0

@register.filter(name='noPrice')
def noPrice(prod):
    if not prod.price:
        return True
    else:
        return False
    
@register.filter(name='prodTotal')
def prodTotal(prod, cart):
    return prod.price * prodQuantity(prod.id, cart)

@register.filter(name='cartTotal')
def cartTotal(prods, cart):
    sum = 0
    count = 0
    for prod in prods:
        if not prod.price:
            count += 1
        else:
            sum += prodTotal(prod, cart)
    if count > 0:
        theTotal = f'${sum} + Custom Items'
    else:
        theTotal = f'${sum}'
    return theTotal

@register.filter(name='currentOrders')
def currentOrders(orders):
    # print('all cust order',orders)
    currentOrders = []
    for o in orders:
        if o.orderStatus != 'New':
            print('new', o.orderStatus, o.orderNum)
            currentOrders.append(o)
        if o.orderStatus == 'Pending':
            currentOrders.append(o)
        if o.orderStatus == 'In Progress':
            currentOrders.append(o)
        if o.orderStatus == 'Order Items Created':
            currentOrders.append(o)
        if o.orderStatus == 'Shipped':
            currentOrders.append(o)
    # print('all cust curr order',currentOrders)
    return currentOrders

@register.filter(name='finishedOrders')
def finishedOrders(orders):
    finishedOrders = []
    for o in orders:
        if o.orderStatus == 'Delivered':
            print('delivered', o.orderNum)
            finishedOrders.append(o)
        if o.orderStatus == 'Rejected':
            finishedOrders.append(o)
        if o.orderStatus == 'Returned':
            finishedOrders.append(o)
        if o.orderStatus == 'Archived':
            finishedOrders.append(o)
    print('all cust fin order',finishedOrders)
    return finishedOrders
