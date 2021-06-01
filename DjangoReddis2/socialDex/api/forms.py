from django import forms
from django.contrib.auth.models import User
from .models import PostBacheca,CustomUser

class PostBachecaFrom(forms.ModelForm):
    class Meta:
        model= PostBacheca
        fields=('text',)#('author','created_date','text')

class SignInForm(forms.ModelForm):

    class Meta:
        model=CustomUser
        fields =('username','password','is_superuser')
class LoginForm(forms.ModelForm):

    class Meta:
        model=CustomUser
        fields =('username','password')

