# coding=utf-8
# Create your views here.
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.core.mail import send_mail

from models import Zamowienie
from forms import ContactForm


def index(request):
    return render_to_response('index.html',
                              context_instance=RequestContext(request))


def wyloguj(request):
    state = 'Zostałeś wylogowany ze strony lub w ogóle nie jesteś zalogowany, powrót do strony głównej'
    logout(request)
    return render_to_response('login/logout.html', {'state': state},
                              context_instance=RequestContext(request))


@login_required(login_url='/zaloguj/')
def uruchomZmianeZamowienia(request, zamowienie_id):
    z = get_object_or_404(Zamowienie, id=zamowienie_id)
    return render_to_response('menadzer/fakturaZmien.html',
                              {'zamowienie': z},
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

