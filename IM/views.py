# coding=utf-8
# Create your views here.
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.core.mail import send_mail

from models import Zamowienie
from forms import ContactForm, ZamowienieWizard


def index(request):
    return render_to_response('menadzer/index.html')


def uruchomNoweZamowienie(request):
    return render_to_response('wizard/stepInvoice.html', {
        'wizard': ZamowienieWizard.as_view(ZamowienieWizard.get_forms())(request)
    }, context_instance=RequestContext(request))

#    return render_to_response('menadzer/fakturaNowa.html', {'form': form, 'form2': invoiceItemFormSet, 'sent': False},
#        context_instance=RequestContext(request))


def uruchomZmianeZamowienia(request, zamowienie_id):
# try except - instrukcja łapania wyjątku
#1 - wykona się zawsze
#2 - sprawdzenie czy pojawił się wyjątek, w tym wypadku sprawdzany jest wyjątek
#    DoesNotExist
#3 - ta linia wykona się tylko wtedy, gdy nie będzie istaniało zamówienie o danym id
#
# Jeżeli wyjątek się nie pojawi, nie wykona się wcale linia 3 i blok try..except
# zostanie zakończony, to znaczy że bezpośrednio przejdziemy do następnej instrukcji
# po tym bloku (return..)
#    try:
#        zamowienie = Zamowienie.objects.get(id = zamowienie_id) #1
#    except Zamowienie.DoesNotExist:                             #2
#        raise Http404                                           #3
#    return render_to_response('menadzer/fakturaZmien.html', {'zamowienie': zamowienie})
    z = get_object_or_404(Zamowienie, id=zamowienie_id)
    return render_to_response('menadzer/fakturaZmien.html',
                              {'zamowienie': z}
    )


def pokazKontakt(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            msg_content = form.cleaned_data['msg_content']
            sender = form.cleaned_data['sender']
            cc_sender = form.cleaned_data['cc_sender']
            odbiorcy = []
            if cc_sender:
                odbiorcy.append(sender)
            send_mail(subject, msg_content, sender, odbiorcy)
        return render_to_response('kontakt/kontakt.html', {'sent': True})
    else:
        form = ContactForm()

    return render_to_response('kontakt/kontakt.html', {'form': form, 'sent': False},
                              context_instance=RequestContext(request))