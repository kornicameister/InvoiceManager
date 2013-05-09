# coding=utf-8

__author__ = 'Adler'
from django.contrib.formtools.wizard.views import SessionWizardView
from django.forms.models import modelformset_factory, BaseFormSet, BaseModelFormSet
from django.shortcuts import render_to_response
from django import forms

from models import PozycjaZamowienia
from models import Zamowienie


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
            'ilosc': forms.TextInput(attrs={'size': '30'})
        }


class PozycjaZamowieniaFormSet(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super(PozycjaZamowieniaFormSet, self).__init__(*args, **kwargs)
        self.queryset = PozycjaZamowienia.objects.none()

    def get_queryset(self):
        return PozycjaZamowienia.objects.get_empty_query_set()


class ZamowienieWizard(SessionWizardView):
    TEMPLATES = {
        "invoice": 'wizard/stepInvoice.html',
        "invoicePosition": 'wizard/stepInvoicePosition.html'
    }

    @staticmethod
    def get_forms():
        return [
            ("invoice", ZamowienieForm),
            ("invoicePosition", modelformset_factory(PozycjaZamowienia, form=PozycjaZamowieniaForm,
                                                     formset=PozycjaZamowieniaFormSet))
        ]

    def get_template_names(self):
        return [self.TEMPLATES[self.steps.current]]

    def done(self, form_list, **kwargs):
        invoice = None

        for form in form_list:
            if isinstance(form, ZamowienieForm):
                invoice = form.save()
            elif isinstance(form, BaseFormSet):
                for posForm in form.forms:
                    if isinstance(posForm, PozycjaZamowieniaForm):
                        positionData = posForm.cleaned_data
                        positionData.update({'zamowienie': invoice})
                        position = PozycjaZamowienia(**positionData)
                        position.save()
                    else:
                        posForm.save()

        self.storage.reset()

        return render_to_response('wizard/stepDone.html',
                                  {'zamowienie': invoice,
                                   'pozycje': PozycjaZamowienia.objects.filter(zamowienie_id=invoice.pk)})
