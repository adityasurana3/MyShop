from django.shortcuts import render, redirect
from .forms import LoginForm, UserRegistrationForm, PasswordResetForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.db.models.query_utils import Q
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string

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
            next = request.GET.get('next')
            if next:
                return redirect(next)
            return render(request, 'account/register_done.html', {'new_user':new_user})
    else:
        form = UserRegistrationForm()
    return render(request, 'account/register.html', {'form':form})


def logout_user(request):
    logout(request)
    return redirect('account:login')

def forget_password(request):
    if request.user.is_authenticated:
        return HttpResponse("You are already loggedin")
    elif request.method == "POST":
        password_form = PasswordResetForm(request.POST)
        if password_form.is_valid():
            form_email = password_form.cleaned_data['email']
            user_email = User.objects.filter(Q(email=form_email))
            for user in user_email:
                subject = 'Password Reset'
                email_template_name = 'account/password_message.txt'
                parameter = {
                        'email': user.email,
                        'domain': '127.0.0.1:8000',
                        'sitename': 'Ecommerce',
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': default_token_generator.make_token(user),
                        'protocol':'http'

                }
                email = render_to_string(email_template_name, parameter)
                send_mail(subject, email, 'your_account@gmail.com', [user.email], fail_silently=False)
                return redirect('account:password_reset_done')
        else:
            return render(request, 'account/password_reset.html', {'form': password_form})

    else:
        password_form = PasswordResetForm()
        return render(request, 'account/password_reset.html', {'form':password_form})
    
def change_password(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PasswordChangeForm(user=request.user, data=request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                return HttpResponse("Password changes")
        else:
            form = PasswordChangeForm(user=request.user)
        return render(request, 'account/change_password.html', {'form':form})
    else:
        return redirect('account:login')
