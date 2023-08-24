from django.conf import settings
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


def sendOrderEmail(user):
    subject = ''
    message = f''
    email_from = settings.EMAIL_HOST_ORDER_USER
    recipient_list = []
    send_mail(subject, message, email_from, recipient_list)

def genOrderCode():
    N = 4
    res01 = ''.join(random.choices(string.ascii_letters, k=N))
    res02 = ''.join(random.choices(string.ascii_letters, k=N))
    stamp = datetime.date.today()
    orderconfirm = f'{stamp.year}-{res01}-{stamp.day}-{res02}-{stamp.month}'
    print(orderconfirm, stamp, res01, res02)
    return orderconfirm