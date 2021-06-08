from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login

# Create your views here.

def register(response):
    if (response.method == 'POST'):
        form = UserCreationForm(response.POST)
        if (form.is_valid()):
            form.save()
        username = response.POST['username']
        password = response.POST['password1']
        user = authenticate(response, username=username, password=password)
        login(response, user)
        return redirect('/')
    elif (response.user.is_authenticated):
        return redirect('/')
    else:
        form = UserCreationForm()
    return render(response, 'register/register.html', {'form':form})