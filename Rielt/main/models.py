from datetime import date

from django.contrib.auth.models import AbstractUser, User
from django.db import models
import uuid
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver


class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value':self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)


class Employees(models.Model):
    employeeCode = models.UUIDField(default=uuid.uuid4, verbose_name='Код', primary_key=True, )
    FIO = models.CharField(verbose_name='ФИО', max_length=50)
    post = models.CharField(verbose_name='Должность', max_length=50)
    dateOfEmployment = models.DateField(verbose_name='Дата найма')
    address = models.CharField(verbose_name='Адрес', max_length=50)
    tel = IntegerRangeField(verbose_name='Телефон', min_value=100000, max_value=999999)

    def __str__(self):
        return self.FIO

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'


class ClientBuy(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    buyerCode = models.UUIDField(default=uuid.uuid4, verbose_name='Код', primary_key=True)
    fio = models.CharField(verbose_name='ФИО', max_length=50)
    address = models.CharField(verbose_name='Адрес', max_length=50)
    tel = IntegerRangeField(verbose_name='Телефон', min_value=100000, max_value=999999)
    passportCode = models.CharField(validators=[RegexValidator(regex='^.{9}$', message='Длинна = 9', code='nomatch')],
                                    verbose_name='Код поспорта',
                                    help_text='2 буквы и 7 цифр',
                                    max_length=9,
                                    unique=True)
    passportNumber = models.CharField(validators=[RegexValidator(regex='^.{14}$', message='Длинна = 14', code='nomatch')],
                                      verbose_name='Индентификационный номер',
                                      help_text='14 символов',
                                      max_length=14,
                                      unique=True)

    def __str__(self):
        return self.fio

    class Meta:
        verbose_name = 'Клиент покупатель'
        verbose_name_plural = 'Клиенты покупатели'


class ClientSell(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sellerCode = models.UUIDField(default=uuid.uuid4, verbose_name='Код', primary_key=True)
    fio = models.CharField(verbose_name='ФИО', max_length=50)
    address = models.CharField(verbose_name='Адрес', max_length=50)
    tel = IntegerRangeField(verbose_name='Телефон', min_value=100000, max_value=999999)
    passportCode = models.CharField(validators=[RegexValidator(regex='^.{9}$', message='Длинна = 9', code='nomatch')],
                                    verbose_name='Код поспорта',
                                    help_text='2 буквы и 7 цифр',
                                    max_length=9,
                                    unique=True)
    passportNumber = models.CharField(validators=[RegexValidator(regex='^.{14}$', message='Длинна = 14', code='nomatch')],
                                      verbose_name='Индентификационный номер',
                                      help_text='14 символов',
                                      max_length=14,
                                      unique=True)

    def __str__(self):
        return self.fio

    class Meta:
        verbose_name = 'Клиент продавец'
        verbose_name_plural = 'Клиенты продавцы'


class Property(models.Model):
    applicationCode = models.UUIDField(default=uuid.uuid4, verbose_name='Код заявки', primary_key=True)
    dateOfOrder = models.DateField(verbose_name='Дата составления заказа', default=date.today)
    name = models.CharField(verbose_name='Наименование объекта', max_length=50)
    area = IntegerRangeField(verbose_name='Площадь м2', min_value=1)
    rooms = IntegerRangeField(verbose_name='Кол-во комнат', min_value=0)
    address = models.CharField(verbose_name='Адрес', max_length=50)
    price = IntegerRangeField(verbose_name='Цена', min_value=0)
    seller = models.ForeignKey(
        ClientSell,
        verbose_name='Продавец',
        on_delete=models.CASCADE,
        null=True
    )
    ifSelled = models.BooleanField(verbose_name='Состояние продажи', default=False)

    def __str__(self):
        return '%s (%s)' % (self.name, self.applicationCode)

    class Meta:
        verbose_name = 'Недвижимость'
        verbose_name_plural = 'Недвижимость'

    def save(self, *args, **kwargs):
        super(Property, self).save(*args, **kwargs)


class SelledProperty(models.Model):
    contractCode = models.UUIDField(default=uuid.uuid4, verbose_name='Код договора', primary_key=True)
    applicationCode = models.OneToOneField(
        Property,
        verbose_name='Код заявки',
        on_delete=models.CASCADE,
        null=True
    )
    employee = models.ForeignKey(
        Employees,
        verbose_name='Сотрудник',
        on_delete=models.CASCADE,
        null=True
    )
    buyer = models.ForeignKey(
        ClientBuy,
        verbose_name='Покупатель',
        on_delete=models.CASCADE,
        null=True
    )
    dateOfOperation = models.DateField(verbose_name='Дата операции', default=date.today)
    profit = models.IntegerField(verbose_name='Прибыль')

    def __str__(self):
        a = self.contractCode
        return str(a)

    class Meta:
        verbose_name = 'Совершенная сделка'
        verbose_name_plural = 'Совершенные сделки'

    def save(self, *args, **kwargs):
        super(SelledProperty, self).save(*args, **kwargs)


class DealsBackup(models.Model):
    create_date = models.DateTimeField(auto_now=True)
    contractCode = models.CharField(verbose_name='Код договора', max_length=100)
    applicationCode = models.CharField(verbose_name='Код заявки', max_length=100)
    dateOfOrder = models.DateField(verbose_name='Дата составления заказа')
    dateOfOperation = models.DateField(verbose_name='Дата операции')
    employee = models.CharField(verbose_name='Сотрудник', max_length=50)
    buyer = models.CharField(verbose_name='Покупатель', max_length=50)
    seller = models.CharField(verbose_name='Продавец', max_length=50)
    price = models.CharField(verbose_name='Цена', max_length=50)
    profit = models.CharField(verbose_name='Прибыль', max_length=50)

    def __str__(self):
        return '%s (%s)' % (self.create_date, self.applicationCode)

    class Meta:
        verbose_name = 'Резервная копия сделки'
        verbose_name_plural = 'Резервные копии сделок'


@receiver(post_save, sender=SelledProperty, dispatch_uid="update_property")
def update_property(sender, created, instance, **kwargs):
    if created:
        aplcode = str(instance.applicationCode)
        x1 = aplcode.find("(")
        x2 = aplcode.find(")")
        x = aplcode[x1 + 1: x2]
        prop = Property.objects.get(applicationCode=x)
        prop.ifSelled = True
        prop.save()
