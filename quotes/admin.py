#!/usr/bin/python

from django.contrib import admin
from quotes.models import Quote

class QuoteAdmin(admin.ModelAdmin):
    fields = ['created', 'quote']
    list_display = ('created', 'quote')
    search_fields = ['quote']
    ordering = ('-created',)
    readonly_fields = ('created', 'quote')

admin.site.register(Quote, QuoteAdmin)
