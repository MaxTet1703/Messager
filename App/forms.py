from django import forms
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.formfields import PhoneNumberField as PNF

from .models import *


class UserLogin(forms.Form):
    number = PNF(region="RU", widget=forms.TextInput(
        attrs={'class': 'number', 'placeholder': 'Ваш номер телефона', 'id': 'number_log'}))

    password = forms.CharField(max_length=30, widget=forms.PasswordInput(attrs={
        'class': 'password',
        'placeholder': 'Введите пароль'}))


class UserCreate(UserCreationForm):
    password1 = forms.CharField(max_length=30, widget=forms.PasswordInput(attrs={
        'class': 'password',
        'placeholder': 'Придумайте пароль'
    }))
    password2 = forms.CharField(max_length=30, widget=forms.PasswordInput(attrs={
        'class': 'password',
        'placeholder': 'Повторите пароль'
    }))

    class Meta:
        model = Users
        fields = ("first_name", "last_name", "number")
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'first_name',
                "placeholder": "Введите ваше имя"
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'last_name',
                "placeholder": "Введите вашу фамилию"
            }),
            "number": forms.NumberInput(attrs={
                'class': 'number', 'placeholder': 'Введите Ваш номер телефона'
            })
        }

    def clean_number(self):
        number = self.data["number"]
        if Users.objects.filter(number=number).exists():
            raise ValidationError("Аккаунт с такми номером уже существует")
        if str(number)[0] != "+":
            raise ValidationError("Нет '+' перед набором номера ")
        if not str(number)[1::].isdigit():
            raise ValidationError("Неверный формат данных")
        return number

    def clean_first_name(self):
        first_name = self.data["first_name"]
        if not first_name.isalpha():
            raise ValidationError("Имя должно содержать только буквы")
        if not first_name:
            raise ValidationError("Заполните это поле")
        return first_name

    def clean_last_name(self):
        last_name = self.data["last_name"]
        if not last_name.isalpha():
            raise ValidationError("Фамилия должна содержать только буквы")
        if not last_name:
            raise ValidationError("Заполните это поле")
        return last_name

    def clean_password1(self):
        password1 = self.data["password1"]
        password2 = self.data["password2"]
        if str(password1).strip() != str(password2).strip():
            raise ValidationError("Пароли не совпадают")
        return password1

    def clean_password2(self):
        password1 = self.data["password1"]
        password2 = self.data["password2"]
        if str(password1).strip() != str(password2).strip():
            raise ValidationError("Пароли не совпадают")
        return password2
