from django.urls import path
from rest_framework import routers
from . import views
from .views import EmployeesViewSet


router = routers.SimpleRouter()
router.register('api/employees', EmployeesViewSet)

urlpatterns = [
    path('', views.index, name='home'),
    path('property', views.property, name='property'),
    path('requests', views.requests, name='requests'),

    path('tables', views.tables, name='tables'),
    path('staff_deals', views.staff_deals, name='staff_deals'),
    path('delete/<str:pk>', views.delete, name='delete'),
    path('update/<str:pk>', views.MyUpdateView.as_view(), name='update'),
    path('backup/<str:pk>', views.backup, name='backup'),

    path('user_reg', views.RegisterUserView.as_view(), name='user_reg'),
    path('login_user', views.UserLoginView.as_view(), name='login_user'),
    path('login_staff', views.StaffLoginView.as_view(), name='login_staff'),
    path('logout', views.MyProjectLogout.as_view(), name='logout'),

    path('user', views.user, name='user'),

    path('create_seller', views.create_seller, name='create_seller'),
    path('create_buyer', views.create_buyer, name='create_buyer'),
    path('create_prop', views.create_prop, name='create_prop'),

    path('delete_prop/<str:pk>', views.delete_prop, name='delete_prop'),
    path('delete_buy/<str:pk>', views.delete_buy, name='delete_buy'),
    path('delete_sell/<str:pk>', views.delete_sell, name='delete_sell'),

    path('update_prop/<str:pk>', views.update_prop, name='update_prop'),
    path('update_buy/<str:pk>', views.update_buy, name='update_buy'),
    path('update_sell/<str:pk>', views.update_sell, name='update_sell'),

    # path('test', views.test, name='test'),
]

urlpatterns += router.urls