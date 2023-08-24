from django.conf import settings
from django.core.mail import send_mail
import datetime



def sendSignupEmail(user):
    subject = 'A Kowabunga Hooker Welcome'
    message = f'Hi {user.firstName}, thank you for registering for Kowabunga Hooker. I am thrilled you found me and chose to sign up.  Feel free to email me with any questions you might have.  I look forward to your 1st order'
    email_from = settings.EMAIL_HOST_MAIN_USER
    recipient_list = [user.email, settings.EMAIL_HOST_MAIN_USER]
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