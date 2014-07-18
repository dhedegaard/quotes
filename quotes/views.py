from django.shortcuts import render

from .models import Quote
from .filters import QuoteFilter


def random(request):
    return render(request, 'quotes/index.html', {
        'quotes': QuoteFilter(
            queryset=Quote.objects.all().extra(order_by='?')),
        'random': True,
        'quotecount': Quote.objects.count(),
    })


def index(request, page=1):
    '''
    This method is used as a url handler for django.
    '''
    quotes = QuoteFilter(request.GET, queryset=Quote.objects.all())

    return render(request, 'quotes/index.html', {
        'quotes': quotes,
        'quotecount': Quote.objects.count(),
    })
