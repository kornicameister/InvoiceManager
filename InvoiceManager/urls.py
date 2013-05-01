from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from IM.forms import ZamowienieWizard

admin.autodiscover()

urlpatterns = patterns('IM.views',
                       url(r'^$', 'index'),
                       url(r'^kontakt/$', 'pokazKontakt'),
                       url(r'^zaloguj/$', 'zaloguj'),
                       url(r'^faktura/edycja/(?P<zamowienie_id>\d+)', 'uruchomZmianeZamowienia'),
                       url(r'^faktura/nowa/$', ZamowienieWizard.as_view(ZamowienieWizard.get_forms())),
                       url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
                       url(r'^admin/', include(admin.site.urls)),
)
