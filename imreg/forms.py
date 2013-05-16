from django import forms
from registration.forms import RegistrationFormUniqueEmail, RegistrationFormTermsOfService


class RegistrationFormUniqueEmailAndTos(RegistrationFormUniqueEmail, RegistrationFormTermsOfService):
    companyName = forms.CharField(max_length=255, label=u'Firma', required=True,
                                  widget=forms.TextInput(attrs={'size': '55'}))
    companyNip = forms.CharField(max_length=255, label=u'NIP', required=True,
                                 widget=forms.TextInput(attrs={'size': '55'}))
    companyRegon = forms.CharField(max_length=255, label=u'REGON', required=True,
                                   widget=forms.TextInput(attrs={'size': '55'}))