# coding=utf-8
from django.db import models
from django.template import Template, Context


class Klient(models.Model):
    STALY = 'S'
    NOWY = 'N'
    KLIENT_TYP = (
        (STALY, 'klient stały'),
        (NOWY, 'klient nowy'),
    )
    nazwa = models.CharField(max_length=20, primary_key=True)
    firma = models.CharField(max_length=20, db_index=True)
    nip = models.CharField(max_length=13, unique=True)
    regon = models.CharField(max_length=14, unique=True)
    typ = models.CharField(max_length=1, choices=KLIENT_TYP, default=NOWY)

    def __unicode__(self):
        return self.nazwa + ' [' + self.typ + ']'

    def czyStaly(self):
        return self.typ == self.STALY


class Adres(models.Model):
    klient = models.OneToOneField(Klient, primary_key=True)
    miasto = models.CharField(max_length=30, db_index=True)
    kodPocztowy = models.CharField(max_length=6, verbose_name='Kod pocztowy', db_index=True)
    ulica = models.CharField(max_length=30)
    nrBudynku = models.CharField(max_length=5, verbose_name='Numer budynku')

    def __unicode__(self):
        return self.klient_id + ' [' + self.miasto + ',' + self.kodPocztowy + ']'


class DaneKontaktowe(models.Model):
    TELEFON = 'T'
    MAIL = 'M'
    DANE_TYP = (
        (TELEFON, 'telefon'),
        (MAIL, 'email'),
    )
    kontakt = models.CharField(max_length=30, unique=True)
    typ = models.CharField(max_length=1, choices=DANE_TYP)
    klient = models.ForeignKey(Klient)

    def __unicode__(self):
        return '[' + self.klient.nazwa + '] = ' + self.kontakt


class Zamowienie(models.Model):
    DATA_FORMAT = '%m/%d/%Y'
    GOTOWKA = 'G'
    PRZELEW = 'P'
    PLATNOSC_TYP = (
        (GOTOWKA, 'gotówka'),
        (PRZELEW, 'przelew'),
    )
    data_w = models.DateField('Data wystawienia', 'dw', db_index=True)
    data_r = models.DateTimeField('Data realizacji', 'dr')
    uwagi = models.CharField(max_length=1000)
    klient = models.ForeignKey(Klient)
    platnosc = models.CharField(max_length=1, choices=PLATNOSC_TYP, db_index=True)

    def __unicode__(self):
        template = Template("Zamowienie {{id}} / {{klient}}")
        context = Context(
            {
                'id': self.id,
                'klient': self.klient.firma
            }
        )
        return template.render(context)
        #TODO wykminic jak ma się ładnie wypisywac w panelu


class Produkt(models.Model):
    klucz = models.CharField(max_length=5, primary_key=True)
    opis = models.CharField(max_length=200)

    def __unicode__(self):
        return self.klucz


class PozycjaZamowienia(models.Model):
    ILOSC_SZTUKI = 'SZT'
    ILOSC_SKRZYNKI = 'SK'
    ILOSC_RODZAJ = (
        (ILOSC_SZTUKI, 'Sztuk'),
        (ILOSC_SKRZYNKI, 'Skrzynek'),
    )
    ##########################################
    PALETY = 'P'
    LUZ = 'L'
    WYMAGANIA_WLASNE = 'WW'
    TRANSPORT = (
        (PALETY, 'Palety po 9000 sztuk'),
        (LUZ, 'Transport luzem'),
        (WYMAGANIA_WLASNE, 'Podaj wymagania własne'),
    )
    ###########################################
    KLATKOWE = 'K'
    SCIOLKOWE = 'S'
    JAJKO_RODZAJ = (
        (SCIOLKOWE, 'Ściółkowe'),
        (KLATKOWE, 'Klatkowe'),
    )
    ###########################################
    zamowienie = models.ForeignKey(Zamowienie)
    produkt = models.ForeignKey(Produkt, verbose_name='Produkt')
    rodzaj = models.CharField(verbose_name='Rodzaj', max_length=2, choices=JAJKO_RODZAJ, default=KLATKOWE,
                              db_index=True)
    ilosc = models.IntegerField(verbose_name='Ilość')
    ilosc_typ = models.CharField(max_length=3, choices=ILOSC_RODZAJ, default=ILOSC_SKRZYNKI, db_index=True,
                                 verbose_name='Opakowanie')
    transport = models.CharField(max_length=100, choices=TRANSPORT, verbose_name='Transport')

    def setInvoice(self, zamowienie=None):
        if zamowienie is None:
            return
        self.zamowienie.set_attributes_from_rel(zamowienie)

    def __unicode__(self):
        return str(self.ilosc) + '[' + str(self.ilosc_typ) + ']'



