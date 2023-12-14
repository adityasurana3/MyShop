from django import forms 
from django.contrib.auth.models import User
from .models import Profile

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password', 'password2']
    
    def clean(self):
        cleaned_data = super(UserRegistrationForm, self).clean()
        password = cleaned_data['password']
        passowrd2 = cleaned_data['password2']
        if password != passowrd2:
            raise forms.ValidationError("Passowrd don\'t match")

    def clean_email(self):
         email = self.cleaned_data['email']
         if User.objects.filter(email=email).exists():
             raise forms.ValidationError("Email already exists")
         return email
    
    
class ProfileForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    class Meta:
        model = Profile
        fields = ['date_of_birth', 'image']

class PasswordResetForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email):
            print("Raised error")
            raise forms.ValidationError("Your email is not registered in our website")
        return email
    
class UserEditForm(forms.ModelForm):
    # username = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        self.fields['username'].disabled = True

    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email']