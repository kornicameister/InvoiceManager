from django import template
from IM.models import Zamowienie

register = template.Library()


@register.simple_tag
def renderPlatnosc(platnosc):
    for k, v in Zamowienie.PLATNOSC_TYP:
        if k == platnosc:
            return v