from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import UpdateView, DeleteView, CreateView
from .models import Employees, ClientBuy, ClientSell, Property, SelledProperty, DealsBackup
from rest_framework import viewsets
from .serializers import EmployeesSerializer
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from .forms import SellForm, BuyForm, PropForm, FindAddress, FindRooms, FindArea, FindPrice, AuthUserForm, \
    SelledPropForm, RegisterUserForm, UserForm, PropUpdateForm
from django.contrib.messages.views import SuccessMessageMixin


# serializer for API
class EmployeesViewSet(viewsets.ModelViewSet):
    queryset = Employees.objects.all()
    serializer_class = EmployeesSerializer


class RegisterUserView(CreateView):
    model = User
    template_name = 'main/user_reg.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('user')
    success_msg = 'Пользователь успешно создан'

    def form_valid(self, form):
        form_valid = super().form_valid(form)
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        aut_user = authenticate(username=username, password=password)
        login(self.request, aut_user)
        return form_valid


class UserLoginView(LoginView):
    template_name = 'staff/login.html'
    form_class = AuthUserForm
    success_url = reverse_lazy('user')

    def get_success_url(self):
        return self.success_url


class StaffLoginView(LoginView):
    template_name = 'staff/login.html'
    form_class = AuthUserForm
    success_url = reverse_lazy('tables')

    def get_success_url(self):
        return self.success_url


class MyProjectLogout(LogoutView):
    next_page = reverse_lazy('home')


# главная страница
def index(request):
    return render(request, 'main/index.html', )


# недвижимость
def property(request):
    property = Property.objects.filter(ifSelled=False)
    return render(request, 'main/property.html', {
        'property': property,
    })


# поиск квартир
def requests(request):
    submitbutton = request.POST.get("submit")

    price = None
    area = None
    address = None
    rooms = None
    property = ''

    form1 = FindAddress(request.POST or None)
    form2 = FindRooms(request.POST or None)
    form3 = FindArea(request.POST or None)
    form4 = FindPrice(request.POST or None)
    if form1.is_valid() and form2.is_valid() and form3.is_valid() and form4.is_valid():
        address = form1.cleaned_data.get("address")
        rooms = form2.cleaned_data.get("rooms")
        area = form3.cleaned_data.get("area")
        price = form4.cleaned_data.get("price")
        if area is None:
            area = 1
        if price is None:
            price = 9 * 10 ** 10
        if rooms is not None and address is not None:
            property = Property.objects.filter(address__contains=address, rooms=rooms, ifSelled=False,
                                               area__gte=area, price__lte=price)
        elif rooms is not None:
            property = Property.objects.filter(rooms=rooms, ifSelled=False,
                                               area__gte=area, price__lte=price)
        elif address is not None:
            property = Property.objects.filter(address__contains=address, ifSelled=False,
                                               area__gte=area, price__lte=price)
        else:
            property = Property.objects.filter(ifSelled=False)

    context = {'form1': form1,
               'form2': form2,
               'form3': form3,
               'form4': form4,
               'submitbutton': submitbutton,
               'property': property,
               'address': address,
               'rooms': rooms,
               'area': area,
               'price': price,
               }

    return render(request, 'main/requests.html', context)


# личный кабинет
def user(request):

    prop = {}
    buyprop = {}
    sellprop = {}

    if request.user.is_authenticated:
        try:
            sellpk = str(request.user.clientsell.pk)
            prop = Property.objects.filter(seller=sellpk)
        except Exception as e1:
            prop = None
        try:
            buypk = str(request.user.clientbuy.pk)
            buyprop = SelledProperty.objects.filter(buyer=buypk).\
                prefetch_related('applicationCode__seller__property_set')
        except Exception as e2:
            buyprop = None
        try:
            sellpk = str(request.user.clientsell.pk)
            sellprop = SelledProperty.objects.filter(seller=sellpk)
        except Exception as e3:
            sellprop = None

    context = {
        'prop': prop,
        'buyprop': buyprop,
        'sellprop': sellprop,
    }
    return render(request, 'main/user.html', context)


# для продавцов\покупателей
def create_buyer(request):
    error_buy = ''
    if request.method == 'POST':
        form_buy = BuyForm(request.POST or None)
        if form_buy.is_valid():
            form_buy.save()
            messages.success(request, "Успешно")
            return redirect('user')
        else:
            error_buy = 'Форма была неверной'
    form_buy = BuyForm()
    context = {
        'form_buy': form_buy,
        'error_buy': error_buy,
    }
    return render(request, 'main/create_buyer.html', context)


# для продавцов\покупателей
def create_seller(request):
    error_sell = ''
    if request.method == 'POST':
        form_sell = SellForm(request.POST)
        if form_sell.is_valid():
            form_sell.save()
            messages.success(request, "Успешно")
            return redirect('user')
        else:
            error_sell = 'Форма была неверной'
    form_sell = SellForm
    context = {
        'form_sell': form_sell,
        'error_sell': error_sell,
    }
    return render(request, 'main/create_seller.html', context)


# добавление недвижимости
def create_prop(request):
    error_prop = ''
    if request.method == 'POST':
        form_prop = PropForm(request.POST)
        if form_prop.is_valid():
            form_prop.save()
            messages.success(request, "Успешно")
            return redirect('user')
        else:
            error_prop = 'Форма была неверной'
    form_prop = PropForm()
    context = {
        'form_prop': form_prop,
        'error_prop': error_prop,
    }
    return render(request, 'main/create_prop.html', context)


# таблицы
def tables(request):
    property = Property.objects.all()
    client_sell = ClientSell.objects.all()
    client_buy = ClientBuy.objects.all()
    selled_prop = SelledProperty.objects.prefetch_related('applicationCode__seller__property_set')

    return render(request, 'staff/tables.html', {
        'property': property,
        'client_sell': client_sell,
        'client_buy': client_buy,
        'selled_prop': selled_prop,
    })


# сделки
def staff_deals(request):
    selled_prop = SelledProperty.objects.all()
    error = ''
    if request.method == 'POST':
        form = SelledPropForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Сделка добавлена")
        else:
            error = 'Форма была неверной'

    form = SelledPropForm()
    context = {
        'form': form,
        'error': error,
        'selled_prop': selled_prop,
    }

    return render(request, 'staff/staff_deals.html', context)


# для кнопки удалить
def delete(request, pk):
    get_selled_prop = SelledProperty.objects.get(pk=pk)
    get_selled_prop.delete()

    return redirect(reverse('staff_deals'))


def delete_prop(request, pk):
    get_prop = Property.objects.get(pk=pk)
    get_prop.delete()

    return redirect(reverse('user'))


def delete_buy(request, pk):
    get_buy = ClientBuy.objects.get(pk=pk)
    get_buy.delete()

    return redirect(reverse('user'))


def delete_sell(request, pk):
    get_sell = ClientSell.objects.get(pk=pk)
    get_sell.delete()

    return redirect(reverse('user'))


# для кнопки обновить
class MyUpdateView(SuccessMessageMixin, UpdateView):
    model = SelledProperty
    template_name = 'staff/staff_deals.html'
    form_class = SelledPropForm
    success_url = reverse_lazy('staff_deals')
    success_message = 'Запись успешно обновлена'

    def get_context_data(self, **kwargs):
        kwargs['update'] = True
        return super().get_context_data(**kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        return kwargs


def update_prop(request, pk):
    if request.method == 'POST':
        prop = Property.objects.get(pk=pk)
        prop_form = PropUpdateForm(request.POST, instance=prop)
        if prop_form.is_valid():
            prop_form.save()
            messages.success(request, 'Запись успешно изменена!')
            return redirect('user')
        else:
            messages.error(request, 'Ошибка')
    prop = Property.objects.get(pk=pk)
    prop_form = PropUpdateForm(instance=prop)
    return render(request, 'main/update_prop.html', {
        'form': prop_form
    })


def update_buy(request, pk):
    if request.method == 'POST':
        buy = ClientBuy.objects.get(pk=pk)
        buy_form = BuyForm(request.POST, instance=buy)
        if buy_form.is_valid():
            buy_form.save()
            messages.success(request, 'Запись успешно изменена!')
            return redirect('user')
        else:
            messages.error(request, 'Ошибка')
    buy = ClientBuy.objects.get(pk=pk)
    buy_form = BuyForm(instance=buy)
    return render(request, 'main/update_buy.html', {
        'form': buy_form
    })


def update_sell(request, pk):
    if request.method == 'POST':
        sell = ClientSell.objects.get(pk=pk)
        sell_form = SellForm(request.POST, instance=sell)
        if sell_form.is_valid():
            sell_form.save()
            messages.success(request, 'Запись успешно изменена!')
            return redirect('user')
        else:
            messages.error(request, 'Ошибка')
    sell = ClientSell.objects.get(pk=pk)
    sell_form = SellForm(instance=sell)
    return render(request, 'main/update_sell.html', {
        'form': sell_form
    })


# для кнопки резервного копирования
def backup(request, pk):
    backupqs = SelledProperty.objects.prefetch_related('applicationCode__seller__property_set').get(pk=pk)
    b = DealsBackup(contractCode=backupqs.contractCode,
                    applicationCode=backupqs.applicationCode,
                    dateOfOrder=backupqs.applicationCode.dateOfOrder,
                    dateOfOperation=backupqs.dateOfOperation,
                    employee=backupqs.employee,
                    buyer=backupqs.buyer,
                    seller=backupqs.applicationCode.seller,
                    price=backupqs.applicationCode.price,
                    profit=backupqs.profit,
                    )
    b.save()
    return redirect(reverse('staff_deals'))
