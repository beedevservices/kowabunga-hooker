from django.core.mail import EmailMessage
from django.conf import settings
from django.urls import reverse
from django.core.mail import send_mail
import datetime
import string
import random



def sendSignupEmail(user):
    subject = 'A Kowabunga Hooker Welcome'
    message = f'Hi {user.firstName}, thank you for registering for Kowabunga Hooker. I am thrilled you found me and chose to sign up.  Feel free to email me with any questions you might have.  I look forward to hearing from you.'
    email_from = settings.EMAIL_HOST_MAIN_USER
    recipient_list = [user.email, ]
    send_mail( subject, message, email_from, recipient_list )

def checkAge(user):
    age = user.age
    today = datetime.date.today()
    adult = today.year - age.year - ((today.month, today.day) < (age.month, age.day))
    print(age, today, adult)
    if adult >= 21:
        isAdult = True
    else:
        isAdult = False
    return isAdult

def test(user, order):
    invoiceUrl = reverse('invoice', args=[order.id])
    updatedUrl = f'http://127.0.0.1:8000{settings.MEDIA_URL}invoices/{order.orderNum}.pdf'
    print('user', user, 'user.firstName', user.firstName, 'order', order, 'order.orderNum', order.orderNum, 'invoiceUrl', invoiceUrl, 'updatedUrl', updatedUrl)


def sendOrderEmail(user,order):
    invoiceUrl = f'http://127.0.0.1:8000{settings.MEDIA_URL}invoices/{order.orderNum}.pdf'
    subject = f'Thank you, {user.firstName} for your order'
    message = f'{user.firstName}, thank you for placing an order.  This is your confirmation email\n Your order number is: {order.orderNum}\n Your current order total is: {order.orderTotal}\n\nI will reach out with the next steps soon.\n\nPlease find a link to your order below.\nhttp://127.0.0.1:8000{settings.MEDIA_URL}invoices/{order.orderNum}.pdf\n\nThe Kowabunga Hooker\n\nkaila@kowabunga-hooker.com\n\nhttps://kowabunga-hooker.com'
    email_from = settings.EMAIL_HOST_ORDER_USER
    recipient_list = [user.email, settings.EMAIL_HOST_ORDER_USER]
    email = EmailMessage(subject, message, email_from, recipient_list)
    email.send()
