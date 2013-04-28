# coding=utf-8
from django.contrib.formtools.wizard.views import  CookieWizardView
from django.shortcuts import render_to_response
from models import PozycjaZamowienia
from models import Zamowienie

__author__ = 'Adler'
from django import forms

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=255, label=u'Temat', required=True,
        widget=forms.TextInput(attrs={'size': '55'}))
    msg_content = forms.CharField(widget=forms.Textarea, label=u'Treść wiadomości', required=True)
    sender = forms.EmailField(label=u'Twój adres email', required=True, widget=forms.TextInput(attrs={'size': '55'}))
    cc_sender = forms.BooleanField(required=False, label=u'Wyślij mi kopię tego emaila')


class ZamowienieForm(forms.ModelForm):
    class Meta:
        model = Zamowienie


class PozycjaZamowieniaForm(forms.ModelForm):
    class Meta:
        model = PozycjaZamowienia
        exclude = ('zamowienie',)
        widgets = {
            'ilosc': forms.TextInput(attrs={'size': '5'})
        }


class ZamowienieWizard(CookieWizardView):
    @staticmethod
    def get_forms():
        return [ZamowienieForm, PozycjaZamowieniaForm]

    def get_template_names(self):
        return ['menadzer/wizard/stepDone.html']

    def done(self, form_list, **kwargs):
        print('Step done reached...')
        return render_to_response('menadzer/wizard/stepDone.html')
