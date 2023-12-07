from django import forms 
from django.contrib.auth.models import User

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
             