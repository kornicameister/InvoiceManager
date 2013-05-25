from django_tables2 import tables
from IM.models import PozycjaZamowienia


class PozycjaZamowieniaTable(tables.Table):
    class Meta:
        model = PozycjaZamowienia
        exclude = {
            'zamowienie',
            'id'
        }
        attrs = {
            'class': 'invoiceItems'
        }