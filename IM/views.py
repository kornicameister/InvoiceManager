# coding=utf-8
# Create your views here.
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.core.mail import send_mail
from django_tables2 import RequestConfig
from IM.models import Klient, Zamowienie, PozycjaZamowienia
from IM.viewModels import PozycjaZamowieniaTable

from forms import ContactForm


def index(request):
    return render_to_response('index.html',
                              context_instance=RequestContext(request))


def wyloguj(request):
    state = 'Wylogowałeś się z aplikacji'
    logout(request)
    return render_to_response('registration/login.html', {'state': state, 'logout': True, 'next': '/'},
                              context_instance=RequestContext(request))


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


@login_required(login_url='/zaloguj/')
def faktury(request, user_name):
    klient = get_object_or_404(Klient, nazwa=user_name)
    zamowienia = Zamowienie.objects.filter(klient=klient)
    resp = {}

    for zam in zamowienia:
        resp[zam] = PozycjaZamowieniaTable(PozycjaZamowienia.objects.filter(zamowienie=zam))
        RequestConfig(request).configure(resp[zam])

    return render_to_response('invoices/invoices.html',
                              {
                                  'klient': klient,
                                  'resp': resp
                              },
                              context_instance=RequestContext(request))