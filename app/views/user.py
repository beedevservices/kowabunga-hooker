from django.shortcuts import render, redirect
from django.contrib import messages
from app.models import *
from app.general import *

def logReg(request):
    return render(request, 'logReg.html')

def register(request):
    if request.method == 'GET':
        return redirect('/logReg/')
    errors = User.objects.validate(request.POST)
    if errors:
        for e in errors.values():
            messages.error(request, e)
        return redirect('/logReg/')
    hashedPw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
    newUser = User.objects.create(
        firstName = request.POST['firstName'],
        lastName = request.POST['lastName'],
        username = request.POST['username'],
        password = hashedPw
    )
    request.session['user_id'] = newUser.id
    if request.POST['regCode'] == SUPERADMINKEY:
        toUpdate = User.objects.get(id=request.session['user_id'])
        toUpdate.level=24
        toUpdate.save()
        return redirect('/theAdmin/')
    if request.POST['regCode'] == ADMINKEY:
        toUpdate = User.objects.get(id=request.session['user_id'])
        toUpdate.level=9
        toUpdate.save()
        return redirect('/theAdmin/')
    else:
        # change this later to customer page
        return redirect('/')

def login(request):
    user = User.objects.filter(username = request.POST['username'])
    if user:
        if user.level == 24:
            userLogin = user[0]
            if brypt.checkpw(request.POSt['password'].encode(), userLogin.password.encode()):
                request.session['user_id'] = userLogin.id
                return redirect('/theAdmin/')
            messages.error(request, 'Invalid Credentials')
            return redirect('/')
        if user.level == 9:
            userLogin = user[0]
            if brypt.checkpw(request.POSt['password'].encode(), userLogin.password.encode()):
                request.session['user_id'] = userLogin.id
                return redirect('/theAdmin/')
            messages.error(request, 'Invalid Credentials')
            return redirect('/')
        else:
            userLogin = user[0]
            if brypt.checkpw(request.POSt['password'].encode(), userLogin.password.encode()):
                request.session['user_id'] = userLogin.id
                return redirect('/')
            messages.error(request, 'Invalid Credentials')
            return redirect('/')
    messages.error(request, 'Username is not in our system')
    return redirect('/')

def logout(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        request.session.clear()
        return redirect('/')