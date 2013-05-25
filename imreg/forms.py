# coding=utf-8
from django import forms
from registration.forms import RegistrationFormUniqueEmail, RegistrationFormTermsOfService

PATTERN_POST = r'^[0-9]{2}-[0-9]{3}$'
FROM_CAPITALIZED = r'^([A-Z]){1}[a-zA-Z]+$'
NIP = r'^(\d{3}[- ]\d{3}[- ]\d{2}[- ]\d{2})|(\d{3}[- ]\d{2}[- ]\d{2}[- ]\d{3})$'
REGON = r'^\d{9}$'
PHONE = r'^[0-9]+-?[0-9]+-?[0-9]+-?[0-9]+-?[0-9]*$'


class RegistrationFormUniqueEmailAndTos(RegistrationFormUniqueEmail, RegistrationFormTermsOfService):
    companyName = forms.RegexField(regex=FROM_CAPITALIZED,
                                   max_length=40,
                                   label=u'Firma',
                                   required=True,
                                   widget=forms.TextInput(attrs={'size': '55'}))
    companyNip = forms.RegexField(regex=NIP,
                                  max_length=16,
                                  label=u'NIP',
                                  required=True,
                                  widget=forms.TextInput(attrs={'size': '55'}))
    companyRegon = forms.RegexField(regex=REGON,
                                    max_length=255,
                                    label=u'REGON',
                                    required=True,
                                    widget=forms.TextInput(attrs={'size': '55'}))
    userFirstName = forms.CharField(max_length=255,
                                    label=u'Imię',
                                    required=True,
                                    widget=forms.TextInput(attrs={'size': '55'}))
    userLastName = forms.CharField(max_length=255,
                                   label=u'Nazwisko',
                                   required=True,
                                   widget=forms.TextInput(attrs={'size': '55'}))
    city = forms.CharField(max_length=255,
                           label=u'Miasto',
                           required=True,
                           widget=forms.TextInput(attrs={'size': '55'}))
    postalCode = forms.RegexField(regex=PATTERN_POST,
                                  max_length=6,
                                  label=u'Kod pocztowy',
                                  required=True,
                                  widget=forms.TextInput(attrs={'size': '55'}))
    street = forms.CharField(max_length=255,
                             label=u'Ulica',
                             required=True,
                             widget=forms.TextInput(attrs={'size': '55'}))
    streetNumber = forms.CharField(max_length=255,
                                   label=u'Numer',
                                   required=True,
                                   widget=forms.TextInput(attrs={'size': '55'}))
    phoneNumber = forms.RegexField(regex=PHONE,
                                   max_length=255,
                                   label=u'Telefon',
                                   required=True,
                                   widget=forms.TextInput(attrs={'size': '55'}))