from django import template

register = template.Library()


@register.filter(name='inTheCart')
def inTheCart(prod, cart):
    keys = cart.keys()
    print(keys, prod)
    for id in keys:
        if int(id) == prod:
            # print('True')
            return True
    return False

@register.filter(name='prodQuantity')
def prodQuantity(prod, cart):
    keys = cart.keys()
    # print(keys)
    for row in keys:
        if int(row) == prod:
            print('quantity filter', cart.get(row))
            return cart.get(row)
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
        theTotal = f'${sum} + Custom Items + Shipping'
    else:
        theTotal = f'${sum} + Shipping'
    return theTotal