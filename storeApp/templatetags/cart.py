from django import template

register = template.Library()


@register.filter(name='inTheCart')
def inTheCart(prod, cart):
    keys = cart.keys()
    # print(keys)
    for row in keys:
        if int(row) == prod:
            # print('True')
            return True
    return False

@register.filter(name='prodQuantity')
def prodQuantity(prod, cart):
    keys = cart.keys()
    for row in keys:
        if int(row) == prod:
            return cart.get(row)
    return 0