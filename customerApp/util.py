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


def sendOrderEmail(user,order):
    subject = f'Thank you, {user.firstName} for your order'
    message = f'{user.firstName}, thank you for placing an order.  This is your confirmation email\n Your order number is: {order.orderNum}\n Your current order total is: {order.orderTotal}\n\nI will reach out with the next steps\n\n\n\nThe Kowabunga Hooker\n\nkaila@kowabunga-hooker.com\n\nhttps://kowabunga-hooker.com'
    email_from = settings.EMAIL_HOST_ORDER_USER
    recipient_list = [user.email, settings.EMAIL_HOST_ORDER_USER]
    send_mail(subject, message, email_from, recipient_list)


# @bg: rgb(233, 219, 206);
# @font: rgb(2, 6, 18);
# @dkpurple: rgb(85, 45, 118);
# @dkgreen: rgb(51, 100, 71);
# @dkred: rgb(152, 28, 75);
# @dkblue: rgb(77, 132, 174);
# @dkbg: rgb(198, 162, 128);
# @ltgreen: rgb(141, 206, 157);
# @ltpink: rgb(251, 187, 216);
# @ltpurple: rgb(220, 204, 243);
# @ltblue: rgb(180, 217, 228);
# @bg: #e9dbce; Quarter Spanish White
# @font: #020612; Dark Green
# @dkpurple: #552d76; Blue Diamond
# @dkgreen: #336447; Hunter Green
# @dkred: #981c4b; Lipstick
# @dkblue: #4d84ae; Steel Blue
# @dkbg: #c6a280; Rodeo Dust
# @ltgreen: #8dce9d;  Chinook
# @ltpink: #fbbbd8; Lavender Pink
# @ltpurple: #dcccf3; Quartz
# @ltblue: #b4d9e4; Powder Blue

# appColors = [(233, 219, 206),(2, 6, 18),(85, 45, 118),(51, 100, 71),(152, 28, 75),(77, 132, 174),(198, 162, 128),(141, 206, 157),(251, 187, 216),(220, 204, 243),(180, 217, 228)]

# def rgbColorName() :
#     colorList = []
#     css3DB = css3_hex_to_names
#     names = []
#     rgbValues = []
#     for color_hex, color_name in css3DB.items():
#         names.append(color_name)
#         rgbValues.append(hex_to_rgb(color_hex))
#     kdt = KDTree(rgbValues)
#     for i in appColors:
#         distance, index = kdt.query(i)
#     print(colorList)
#     return colorList