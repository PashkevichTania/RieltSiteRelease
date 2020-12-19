from django.contrib import admin
from django.urls import path, include
from django.conf.urls import include, url


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    #url(r'^api/v1/', include('main.urls')),
    #url(r'^admin/', admin.site.urls),
]
