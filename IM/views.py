# coding=utf-8
# Create your views here.
from django.contrib.auth import login, authenticate
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.core.mail import send_mail

from models import Zamowienie
from forms import ContactForm


def index(request):
    return render_to_response('index.html')


def zaloguj(request):
    state = "Proszę zalogować się przy użyciu swojego hasła i nazwy użytkownika..."
    username = ''
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                state = "Logowanie zakończyło się sukcesem"
            else:
                state = "Konto użytkownika istnieje, ale jest nieaktywne, proszę skontaktować się z administratorem"
        else:
            state = "Nazwa użytkownika / hasło są niepoprawne"

    return render_to_response('login/login.html', {'state': state, 'username': username},
                              context_instance=RequestContext(request))


def uruchomZmianeZamowienia(request, zamowienie_id):
    z = get_object_or_404(Zamowienie, id=zamowienie_id)
    return render_to_response('menadzer/fakturaZmien.html',
                              {'zamowienie': z})


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