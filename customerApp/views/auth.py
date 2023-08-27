from django.shortcuts import render, redirect
from django.contrib import messages
from customerApp.models import *
from storeApp.models import *
from customerApp.util import *
import bcrypt

def login(request):
    url = request.session['url']
    if not url:
        url = '/'
    user = User.objects.filter(email = request.POST['email'])
    if user:
        userLogin = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), userLogin.password.encode()):
            request.session['user_id'] = userLogin.id
            return redirect(url)
        messages.error(request, 'Invalid Credentials')
        return redirect('/logReg/')
    messages.error(request, 'That Username is not in our system, please register for an account')
    return redirect('/logReg/')

def reg(request):
    url = request.session['url']
    if not url:
        url = '/'
    if request.method == 'GET':
        return redirect('/logReg/')
    errors = User.objects.validate(request.POST)
    if errors:
        for err in errors.values():
            messages.error(request, err)
        return redirect('/logReg/')
    hashedPw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
    newUser = User.objects.create(
        firstName = request.POST['firstName'],
        lastName = request.POST['lastName'],
        age = request.POST['age'],
        email = request.POST['email'],
        password = hashedPw
    )
    request.session['user_id'] = newUser.id
    messages.error(request, f'Welcome {newUser.firstName}')
    sendSignupEmail(newUser)
    return redirect(url)

def profile(request):
    if 'user_id' not in request.session:
        messages.error(request, "you need to be logged in to view this page")
        return redirect('/logReg/')
    else:
        user = User.objects.get(id=request.session['user_id'])
        cart = request.session['cart']
        context = {
            'user': user,
            'cart': cart,
        }
        return render(request, 'profile.html', context)
    
def updateProfile(request):
    toUpdate = User.objects.get(user=request.session['user_id'])
    toUpdate.profile.address01 = request.POST['address01']
    toUpdate.profile.address02 = request.POST['address02']
    toUpdate.profile.city = request.POST['city']
    toUpdate.profile.state = request.POST['state']
    toUpdate.profile.zip = request.POST['zip']
    toUpdate.profile.phone = request.POST['phone']
    toUpdate.save()
    messages.error(request, 'Updated address')
    return redirect('/customer/profile/')