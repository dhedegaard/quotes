#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from quotes.models import Quote
import math

PAGE_SIZE = 20

def index(request, page=1):
    first_index = (page - 1) * PAGE_SIZE
    quotes = Quote.objects.all().order_by('-created')[first_index:first_index + PAGE_SIZE]

    page_count = int(math.ceil(len(Quote.objects.all()) / float(PAGE_SIZE)))

    return render_to_response(
        'quotes/index.html',
        {'title': 'Quotes',
         'quotes': quotes,
         'page': page,
         'page_count': page_count,
         })
