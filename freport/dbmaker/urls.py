from django.conf.urls import url

from . import views
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^balancesheet/$', views.balancesheet ,name='balancesheet'),
    url(r'^$', views.index , name='index')
]
