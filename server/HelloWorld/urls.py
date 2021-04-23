from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^top/$', views.GetSort),
    url(r'^id/$', views.GetIDSort),
    url(r'^register/$', views.Register),
    url(r'^update/$', views.Update),
]