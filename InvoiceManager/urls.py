from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.contrib.auth.decorators import login_required
from IM.forms import ZamowienieWizard

admin.autodiscover()

urlpatterns = patterns('IM.views',
                       url(r'^$', 'index'),
                       url(r'^accounts/', include('imreg.urls')),
                       url(r'^kontakt/$', 'pokazKontakt'),
                       url(r'^polityka/prywatnosci/$', 'politykaPrywatnosci'),
                       url(r'^faktura/klient/(?P<user_name>\w+)$', 'faktury'),
                       url(r'^faktura/nowa/$', login_required(ZamowienieWizard.as_view(ZamowienieWizard.get_forms()),
                                                              login_url="/accounts/login/")),
                       url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
                       url(r'^admin/', include(admin.site.urls)),
)
