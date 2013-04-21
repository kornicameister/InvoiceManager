# coding=utf-8
from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()
urlpatterns = patterns('adler.tutti.controllers',
    (r'^$',
     'index'), #tutaj będzie strona powitalna
    (r'^faktura/nowa/$',
     'uruchomNoweZamowienie'),
    (r'^kontakt/$',
     'pokazKontakt'),
    #tutaj będzie widok nowej faktury
    (r'^faktura/edycja/(?P<zamowienie_id>\d+)',
     'uruchomZmianeZamowienia'),
    #tutaj będzie edycja faktury, w sensie zmiany statusu - potwierdzenie lub anulowanie zamówienia

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
