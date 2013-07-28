import json

from django.http import HttpResponse, HttpResponseBadRequest

from quotes.models import Quote
from views import MAX_PAGE_SIZE
from views import get_random_quotes


def _return_json(request, queryset):
    '''
    Parses 'count' from request.GET or uses default.
    Returns data from queryset as json or returns HTTP 400.
    '''
    try:
        count = int(request.GET.get('count', 20))
    except ValueError:
        return HttpResponseBadRequest('400 Bad parameter: count is not a number: %s' % count)

    if count > MAX_PAGE_SIZE or count < 1:
        return HttpResponseBadRequest('400 Bad parameter: count is too high (above %d) or too low (below 1): %d' % (MAX_PAGE_SIZE, count))

    queryset = queryset[:count]

    return HttpResponse(json.dumps(list([q.quote for q in queryset])))


def rest_random(request):
    '''
    Returns random quotes in a json array.
    Takes a parameter 'count'.
    '''
    quotes = get_random_quotes()
    return _return_json(request, quotes)


def rest_latest(request):
    '''
    Returns the latest queries in a json array.
    Takes a parameter 'count'.
    '''
    quotes = Quote.objects.all().order_by('-created')
    return _return_json(request, quotes)
