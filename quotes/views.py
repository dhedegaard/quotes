from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.html import format_html

from .models import Quote
from .forms import SearchForm
from .filters import QuoteFilter


def random(request):
    return render(request, 'quotes/index.html', {
        'quotes': QuoteFilter(
            queryset=Quote.objects.all().extra(order_by='?')),
        'random': True,
    })


def index(request, page=1):
    '''
    This method is used as a url handler for django.
    '''
    quotes = QuoteFilter(request.GET, queryset=Quote.objects.all())

    return render(request, 'quotes/index.html', {
        'quotes': quotes,
    })