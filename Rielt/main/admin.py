from django.contrib import admin
from .models import Employees, ClientBuy, ClientSell, Property, SelledProperty, DealsBackup


admin.site.register(Employees)
admin.site.register(ClientBuy)
admin.site.register(ClientSell)
admin.site.register(Property)
admin.site.register(SelledProperty)
admin.site.register(DealsBackup)

