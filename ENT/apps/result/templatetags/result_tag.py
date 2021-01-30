from django import template

from ..models import Person

register = template.Library()


@register.simple_tag()
def get_nick():
    a = Person.objects.all()
    return a
