from django.shortcuts import render, redirect
from .forms import LoginForm, UserRegistrationForm, ProfileForm
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
                return render(request, 'account/login.html')
            else:
                return HttpResponse("Something went wrong")
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form':form})

def register(request):
    if request.user.is_authenticated:
        return HttpResponse("You are already loggedin")
    elif request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            return render(request, 'account/register_done.html', {'new_user':new_user})
    else:
        form = UserRegistrationForm()
    return render(request, 'account/register.html', {'form':form})


def logout_user(request):
    logout(request)
    return redirect('login')
