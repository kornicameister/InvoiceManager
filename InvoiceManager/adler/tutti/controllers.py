# coding=utf-8
# Create your views here.
from models import Klient, Zamowienie
from django.shortcuts import render_to_response, get_object_or_404

def index(request):
    return render_to_response('menadzer/index.html')

def uruchomNoweZamowienie(request):
    return render_to_response('menadzer/fakturaNowa.html')

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
    return render_to_response('kontakt/kontakt.html')