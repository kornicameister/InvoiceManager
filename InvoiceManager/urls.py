from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login
from IM.forms import ZamowienieWizard

admin.autodiscover()

urlpatterns = patterns('IM.views',
                       url(r'^$', 'index'),
                       url(r'^kontakt/$', 'pokazKontakt'),
                       url(r'^zaloguj/$', login, {'template_name': 'login/login.html'}),
                       url(r'^wyloguj/$', 'wyloguj'),
                       url(r'^faktura/edycja/(?P<zamowienie_id>\d+)', 'uruchomZmianeZamowienia'),
                       url(r'^faktura/nowa/$', login_required(ZamowienieWizard.as_view(ZamowienieWizard.get_forms()),
                                                              login_url="/zaloguj/")),
                       url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
                       url(r'^admin/', include(admin.site.urls)),
)
