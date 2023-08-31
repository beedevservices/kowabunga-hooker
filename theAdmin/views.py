from django.shortcuts import render, redirect
from django.contrib import messages
from customerApp.models import *
from storeApp.models import *
from customerApp.util import *
import bcrypt
from django.contrib.auth.decorators import user_passes_test, login_required
from django.urls import reverse

def superuser_check(user):
    return user.is_superuser

@user_passes_test(superuser_check, login_url='login')
@login_required
def theAdmin(request):
    invoices = Invoice.objects.all().values()
    context = {
        'invoices': invoices,
    }
    return render(request, 'theAdmin.html', context)

def checkSuperUser(request):
    if request.user.is_authenticated and request.user.is_superuser:
        # If the user is a superuser and authenticated, allow them to proceed
        return redirect('/theAdmin/')  # Replace with your actual view name

    # If the user is not a superuser or not authenticated,
    # store the current URL as the 'next' parameter in the login URL
    next_url = reverse('/theAdmin/')  # Replace with your actual view name
    login_url = reverse('login')
    login_url_with_next = f"{login_url}?next={next_url}"

    return redirect(login_url_with_next)
