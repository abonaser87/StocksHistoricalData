from django.conf.urls import url

from . import views
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^report/(?P<company_id>[0-9]+)/(?P<statement_id>[0-9]+)', views.report, name='statement'),
    url(r'^$', views.index , name='index')
]
