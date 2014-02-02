from django.shortcuts import render
from django.contrib import messages
from django.utils.html import format_html

from .models import Quote
from .forms import SearchForm

PAGE_SIZE = 20


def random(request):
    return render(request, 'quotes/index.html', {
        'quotes': Quote.objects.all().extra(order_by='?')[:PAGE_SIZE],
        'random': True,
        'total_quotes': Quote.objects.count(),
    })


def index(request):
    '''
    This method is used as a url handler for django.
    '''
    quotes = Quote.objects.all()
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data['search']
            quotes = Quote.objects.filter(quote__icontains=search)
            if quotes.count() == 0:
                message = format_html(
                    'No quotes matching the search <b>{0}</b>.', search)
                messages.warning(request, message)
    else:
        form = SearchForm()

    return render(request, 'quotes/index.html', {
        'quotes': quotes[:PAGE_SIZE],
        'total_quotes': Quote.objects.count(),
    })
