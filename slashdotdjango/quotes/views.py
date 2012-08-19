#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import Http404
from quotes.models import Quote
import math

PAGE_SIZE = 20

def _generate_pagelist(page, pagecount, count=PAGE_SIZE):
    '''
    Generates the numbers for the pages displayed in the gui.
    '''
    if pagecount == 0:
        return []
    elif page < count / 2:
        if pagecount > 10:
            return range(1, 10 + 1)
        else:
            return range(1, pagecount)
    elif page > pagecount - (count / 2):
        return range(pagecount - count, pagecount + 1)
    else:
        return range(page - count / 2 + 1, page + count / 2 + 1)

def _search_quotes(search):
    '''
    Returns the quotes fitting the search-pattern based on searching
    according to a postgres searchvector (tsearch2).
    '''
    return Quote.objects.select_related().extra(
        select = {
            'created': 'created',
            'quote': 'quote',
            'rank': 'ts_rank_cd(quote_tsv, plainto_tsquery(%s), 32)',
            },
        where = ['quote_tsv @@ plainto_tsquery(%s)'],
        params = [search],
        select_params= [search],
        ).order_by('-rank')

def index(request, page=1):
    '''
    This method is used as a url handler for django.
    '''

    # handle search parameter, if any
    GET = request.GET
    search = ''
    if 'search' in GET:
        search = GET['search'].strip()
        if len(search) > 0:
            # trim '+' in beginning and end, since that's just space escaped.
            if search[0] == '+':
                search = search[1:]
            if search[-1] == '+':
                search = search[:-1]
    
    # convert page, if it's not an int (ie str)
    if not isinstance(page, int):
        page = int(page)

    # get data, setup content
    first_index = (page - 1) * PAGE_SIZE
    if search:
        quotes = _search_quotes(search)
    else:
        quotes = Quote.objects.all().order_by('-created')

    pagecount = int(math.ceil(quotes.count() / float(PAGE_SIZE))) + 1
    quotes = quotes[first_index:first_index + PAGE_SIZE]

    # if page above pagecount, then 404.
    if page > pagecount and pagecount > 0:
        raise Http404

    # setup the rest of the variables
    pageprev = page - 1
    pagenext = page + 1
    pagelist = _generate_pagelist(page, pagecount)

    # return render from template
    return render_to_response('quotes/index.html', locals())
