from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from userapp.models import User
from mainapp.models import Order
from django import forms
from django.core.exceptions import ValidationError

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

class OrderForm(forms.ModelForm):
    def __init__(self, *args, **kwars):
        super().__init__(*args, **kwars)

    class Meta:
        model = Order
        fields = ['name','adress','email','phone']
        widgets = {
            'name': forms.TextInput(attrs={'class':'order-input'}),
            'adress': forms.TextInput(attrs={'class':'order-input', 'id':'adress'}),
            'email': forms.EmailInput(attrs={'class':'order-input'}),
            'phone': forms.TextInput(attrs={'class':'order-input'}),
        }

    def clean_name(self):
        print('VALID')
        name = self.cleaned_data['name']
        if name != 'Женя':
            raise ValidationError('У вас нет привелегий на то, чтобы тратить деньги')

        return name