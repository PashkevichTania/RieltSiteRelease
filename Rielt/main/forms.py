from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import ClientSell, ClientBuy, Property, SelledProperty
from django.forms import ModelForm, TextInput, NumberInput, ModelChoiceField, DateInput, Select
from django import forms


class RegisterUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')
    def __init__(self,*args, **kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class SellForm(ModelForm):
    class Meta:
        model = ClientSell
        fields = ["user",
                  "fio",
                  "address",
                  "tel",
                  "passportCode",
                  "passportNumber"]
        widgets = {
            "user": Select(attrs={
                'class': 'form-control',
                'placeholder': 'Выберете user',
            }),
            "fio": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите ФИО'
            }),
            "address": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите адрес'
            }),
            "tel": NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите tel'
            }),
            "passportCode": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите код паспорта'
            }),
            "passportNumber": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите индентификационный номер'
            }),
        }


class BuyForm(ModelForm):
    class Meta:
        model = ClientBuy
        fields = ["user",
                  "fio",
                  "address",
                  "tel",
                  "passportCode",
                  "passportNumber"]
        widgets = {
            "fio": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите ФИО'
            }),
            "address": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите адрес'
            }),
            "tel": NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите телефон'
            }),
            "passportCode": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите код паспорта'
            }),
            "passportNumber": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите индентификационный номер',
            }),
        }


class PropForm(ModelForm):
    class Meta:
        model = Property
        fields = ["dateOfOrder",
                  "name",
                  "area",
                  "rooms",
                  "address",
                  "price",
                  "seller"]
        widgets = {
            "dateOfOrder": DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите дату составления заказа (dd.mm.yyyy)'
            }),
            "name": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите наименование'
            }),
            "area": NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите площадь'
            }),
            "rooms": NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите количество комнат'
            }),
            "address": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите адрес'
            }),
            "price": NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите цену'
            }),
            "seller": Select(attrs={
                'class': 'form-control',
                'placeholder': 'Выберете продавца',
            }),
        }


class PropUpdateForm(ModelForm):
    class Meta:
        model = Property
        fields = ["dateOfOrder",
                  "name",
                  "area",
                  "rooms",
                  "address",
                  "price",
                  ]
        widgets = {
            "dateOfOrder": DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите дату составления заказа (dd.mm.yyyy)'
            }),
            "name": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите наименование'
            }),
            "area": NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите площадь'
            }),
            "rooms": NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите количество комнат'
            }),
            "address": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите адрес'
            }),
            "price": NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите цену'
            }),
        }


class FindAddress(forms.Form):
    address = forms.CharField(label='Адрес содержит', max_length=50, required=False)


class FindRooms(forms.Form):
    rooms = forms.IntegerField(label='Количество комнат', required=False)


class FindArea(forms.Form):
    area = forms.IntegerField(label='Минимальная площадь', required=False)


class FindPrice(forms.Form):
    price = forms.IntegerField(label='Максимальная цена', required=False)


class AuthUserForm(AuthenticationForm, forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class SelledPropForm(ModelForm):
    class Meta:
        model = SelledProperty
        fields = ["applicationCode",
                  "employee",
                  "buyer",
                  "dateOfOperation",
                  "profit",
                  ]
        widgets = {
            "applicationCode": Select(attrs={
                'class': 'form-control',
                'placeholder': 'Выберете код заявки',
            }),
            "employee": Select(attrs={
                'class': 'form-control',
                'placeholder': 'Выберете отрудника'
            }),
            "buyer": Select(attrs={
                'class': 'form-control',
                'placeholder': 'Выберете продавца',
            }),
            "dateOfOperation": DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите дату операции (dd.mm.yyyy)'
            }),
            "profit": NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите прибыль'
            }),
        }