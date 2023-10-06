from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from userapp.models import User
from django import forms

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'username-input'}))
    password  = forms.CharField(widget=forms.PasswordInput(attrs={'class':'password-input'}))
    class Meta:
        model = User
        fields = ('username', 'password')

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'firstname-input'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'lastname-input'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'username-input'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'email-input'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'password1-input'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'password2-input'}))
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

class UserProfileForm(UserChangeForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'firstname-input', 'placeholder':'Имя'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'lastname-input', 'placeholder':'Фамилия'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'username-input', 'placeholder':'Логин'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'email-input', 'placeholder':'Email'}))
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')

class OrderForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'firstname-input', 'placeholder':'Имя'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'email-input', 'placeholder':'Email'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'class':'address-input', 'placeholder':'Адрес'}))
    class Meta:
        model = User
        fields = ('first_name', 'email', 'address')