from django.shortcuts import render, redirect
from .forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse


# Create your views here.
def login_user(request):
    if request.user.is_authenticated:
        return HttpResponse("You are logged in")
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request,user)
                return render(request, 'login.html')
            else:
                return HttpResponse("Something went wrong")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form':form})


def logout_user(request):
    logout(request)
    return redirect('login')
