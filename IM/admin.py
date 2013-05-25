# coding=utf-8
__author__ = 'Adler'
from django.contrib import admin
from models import Klient, DaneKontaktowe, Adres, Zamowienie, PozycjaZamowienia, Produkt


class DaneInline(admin.TabularInline):
    model = DaneKontaktowe
    extra = 1


class AdresInline(admin.TabularInline):
    model = Adres
    extra = 1


class KlientAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            'Dane podstawowe',
            {
                'fields': ['nazwa', 'firma', 'typ']
            }
        ),
        (
            'Dane do płatności',
            {
                'fields': ['nip', 'regon']
            }
        ),
    ]
    inlines = [DaneInline, AdresInline]
    list_filter = ['nazwa', 'firma', 'typ']
    search_fields = ['nazwa', 'firma', 'typ']


class DaneAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            'Podaj kontakt',
            {
                'fields': ['kontakt']
            }

        ),
        (
            'Rodzaj kontaktu',
            {
                'fields': ['typ']
            }
        ),
        (
            'Wybierz klienta',
            {
                'fields': ['klient']
            }
        )
    ]
    list_filter = ['typ', 'klient']
    search_fields = ['typ', 'klient']


class PozycjaInline(admin.StackedInline):
    model = PozycjaZamowienia
    extra = 0


class ZamowienieAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            'Podaj daty',
            {
                'fields': ['dw', 'dr']
            }

        ),
        (
            'Wybierz formę płatności dla klienta',
            {
                'fields': ['platnosc', 'klient']
            }
        )
    ]
    inlines = [PozycjaInline]
    list_filter = ['dw', 'dr', 'klient']
    search_fields = ['dw', 'dr', 'klient']
    date_hierarchy = 'dw'


admin.site.register(Klient, KlientAdmin)
admin.site.register(DaneKontaktowe, DaneAdmin)
admin.site.register(Zamowienie, ZamowienieAdmin)
admin.site.register(Produkt)

