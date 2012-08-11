#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from quotes.models import Quote
import math

PAGE_SIZE = 20

def _generate_pagelist(page, page_count, count=20):
    '''
    Generates the numbers for the pages displayed in the gui.
    '''
    if page < count / 2:
        return range(1, count + 1)
    elif page > page_count - (count / 2):
        return range(page_count - count, page_count + 1)
    else:
        return range(page - count / 2 + 1, page + count / 2 + 1)

def index(request, page=1):
    '''
    This method is used as a url handler for django.
    '''
    # convert page, if it's not an int (ie str)
    if not isinstance(page, int):
        page = int(page)

    # get data, setup content
    first_index = (page - 1) * PAGE_SIZE
    quotes = Quote.objects.all().order_by('-created')[first_index:first_index + PAGE_SIZE]
    pagecount = int(math.ceil(len(Quote.objects.all()) / float(PAGE_SIZE)))

    # return render from template
    return render_to_response(
        'quotes/index.html',
        {'quotes': quotes,
         'page': page,
         'pageprev': page - 1,
         'pagenext': page + 1,
         'pagelist': _generate_pagelist(page, pagecount),
         'pagecount': pagecount,
         })
