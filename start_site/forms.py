from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
# from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    # username = forms.CharField(forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    # first_name = forms.CharField(forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
    #                              max_length=32, help_text='First name')
    # last_name = forms.CharField(forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
    #                             max_length=32, help_text='Last name')
    # email = forms.EmailField(forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}), max_length=64,
    #                          help_text='Enter a valid email address')
    # password1 = forms.CharField(forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    # password2 = forms.CharField(forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password Again'}))
    phone_number = forms.CharField(label= 'Номер телефона', help_text='обязательное поле', required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email', 'phone_number')


class SelfUserChangeForm(UserChangeForm):
    # user_tg_id = forms.IntegerField(label= 'Telegram id', help_text='This is not required', required=False)
    phone_number = forms.CharField(label='Номер телефона', required=True)

    class Meta(UserChangeForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone_number')

