from django.contrib.sites.models import Site, RequestSite
from registration import signals
from registration.backends.default.views import RegistrationView
from imreg.models import CRegistrationProfile


class CRegistrationView(RegistrationView):
    def register(self, request, **cleaned_data):

        username = cleaned_data['username']
        email = cleaned_data['email']
        password = cleaned_data['password1']
        companyName = cleaned_data['companyName']
        companyNIP = cleaned_data['companyNip']
        companyREGON = cleaned_data['companyRegon']

        if Site._meta.installed:
            site = Site.objects.get_current()
        else:
            site = RequestSite(request)

        new_user = CRegistrationProfile \
            .objects \
            .create_inactive_user_with_company(username=username,
                                               email=email,
                                               companyName=companyName,
                                               companyNIP=companyNIP,
                                               companyREGON=companyREGON,
                                               password=password,
                                               site=site)

        signals.user_registered.send(sender=self.__class__,
                                     user=new_user,
                                     request=request)
        return new_user