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
        userFirstName = cleaned_data['userFirstName']
        userLastName = cleaned_data['userLastName']
        city = cleaned_data['city']
        postalCode = cleaned_data['postalCode']
        street = cleaned_data['street']
        streetNumber = cleaned_data['streetNumber']
        phoneNumber = cleaned_data['phoneNumber']

        if Site._meta.installed:
            site = Site.objects.get_current()
        else:
            site = RequestSite(request)

        new_user = CRegistrationProfile \
            .objects \
            .create_inactive_user_im(username=username,
                                     firstname=userFirstName,
                                     lastname=userLastName,
                                     password=password,
                                     email=email,
                                     city=city,
                                     cityPostalCode=postalCode,
                                     cityStreet=street,
                                     cityStreetNumber=streetNumber,
                                     companyName=companyName,
                                     companyNIP=companyNIP,
                                     companyREGON=companyREGON,
                                     phoneNumber=phoneNumber,
                                     site=site)

        signals.user_registered.send(sender=self.__class__,
                                     user=new_user,
                                     request=request)
        return new_user