from django import template
from django.template.defaultfilters import stringfilter
from django.utils.html import mark_safe

register = template.Library()


@register.filter(is_safe=True)
@stringfilter
def spacify(value):
    '''
    Converts spaces in the value to &nbsp;, this is to make sure spaces are
    shown as expected.
    '''
    return mark_safe(value.
                     replace('  ', '&nbsp;' * 2).
                     replace('&nbsp; ', '&nbsp;' * 2).
                     replace('\t', '&nbsp;' * 4))