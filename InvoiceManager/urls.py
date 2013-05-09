from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from IM.forms import ZamowienieWizard

admin.autodiscover()

urlpatterns = patterns('IM.views',
                       url(r'^$', 'index'),
                       url(r'^kontakt/$', 'pokazKontakt'),
                       url(r'^zaloguj/$', 'zaloguj'),
                       url(r'^wyloguj/$', 'wyloguj'),
                       url(r'^faktura/edycja/(?P<zamowienie_id>\d+)', 'uruchomZmianeZamowienia'),
                       url(r'^faktura/nowa/$', ZamowienieWizard.as_view(ZamowienieWizard.get_forms())),
                       url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
                       url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()
