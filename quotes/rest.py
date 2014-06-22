import json

from django.http import HttpResponse, HttpResponseBadRequest
from django.utils.html import format_html

from .models import Quote
from .forms import RestForm


def _return_json(request, queryset):
    # Set the default count value, if the argument is missing.
    if 'count' not in request.GET:
        get_params = request.GET.dict()
        get_params['count'] = '20'
        request.GET = get_params

    form = RestForm(request.GET)
    if not form.is_valid():
        # If the form is not valid, format the errors in a sensible way.
        errors = '\n'.join([
            format_html('{0}: {1}', field, error.as_text())
            for field, error in form.errors.items()])
        return HttpResponseBadRequest(
            errors, content_type='text/plain')

    queryset = queryset[:form.cleaned_data['count']]

    return HttpResponse(json.dumps(list([q.quote for q in queryset])))


def rest_random(request):
    return _return_json(
        request, Quote.objects.order_by('?'))


def rest_latest(request):
    return _return_json(
        request, Quote.objects.all().order_by('-created'))
