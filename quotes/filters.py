import django_filters

from .models import Quote


class QuoteFilter(django_filters.FilterSet):
    quote = django_filters.CharFilter(lookup_type='icontains')

    class Meta:
        model = Quote
        fields = ['quote']
