from registration.views import RegistrationView


class RegistrationWithCompany(RegistrationView):
    def register(self, request, **cleaned_data):
        return super(RegistrationWithCompany, self).register(request, **cleaned_data)