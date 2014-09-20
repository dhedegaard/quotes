from __future__ import absolute_import

import datetime
import logging

import mock
from django.test import TestCase
from django.core.urlresolvers import resolve
from django.core.management import call_command

from . import views, rest
from .templatetags.spacify import spacify
from .models import Quote


class ModelsTests(TestCase):

    def test_quote_create(self):
        quote = Quote.objects.create(quote='testquote')

        self.assertIsInstance(quote.id, int)
        self.assertIsInstance(quote.created, datetime.datetime)
        self.assertEqual(quote.quote, 'testquote')

    def test_quote_unicode(self):
        quote = Quote.objects.create(quote='testquote2')

        self.assertEqual(
            str(quote), '[%s, %s, testquote2]' % (
                quote.id, quote.created))


class UrlsTests(TestCase):

    def test_index(self):
        index_page = resolve('/')
        self.assertEqual(index_page.func, views.index)

    def test_index_page(self):
        index_page_page = resolve('/page/10/')
        self.assertEqual(index_page_page.func, views.index)

    def test_random(self):
        random_page = resolve('/random/')
        self.assertEqual(random_page.func, views.random)

    def test_rest_latest(self):
        rest_latest = resolve('/rest/latest/')
        self.assertEqual(rest_latest.func, rest.rest_latest)

    def test_rest_random(self):
        rest_random = resolve('/rest/random/')
        self.assertEqual(rest_random.func, rest.rest_random)


class ViewTests(TestCase):

    def test_index(self):
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quotes/index.html')

    def test_above_max_page(self):
        response = self.client.get('/page/9999999999/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quotes/index.html')

    def test_page_zero(self):
        response = self.client.get('/page/0/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quotes/index.html')

    def test_search(self):
        response = self.client.post('/', {'search': 'test'})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quotes/index.html')

    def test_random(self):
        response = self.client.get('/random/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quotes/index.html')


class RestViewTests(TestCase):

    def setUp(self):
        self.quote = Quote.objects.create(quote='test123')

    def test_rest_random(self):
        response = self.client.get('/rest/random/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, '["test123"]')

    def test_latest(self):
        response = self.client.get('/rest/latest/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, '["test123"]')

    def test_latest_with_count(self):
        response = self.client.get('/rest/latest/?count=1')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, '["test123"]')

    def test_latest_count_above_limit(self):
        response = self.client.get('/rest/latest/?count=300')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.content,
            'count: * Ensure this value is less than or equal to 200.')


class TemplateTagsTests(TestCase):

    def test_spacify(self):
        self.assertEqual(spacify('hej dav'), 'hej dav')

    def test_spacify2(self):
        self.assertEqual(spacify('hej  dav'), 'hej&nbsp;&nbsp;dav')

    def test_spacify3(self):
        self.assertEqual(spacify('hej<br />dav'), 'hej<br />dav')


class GetQuoteCommandTests(TestCase):
    def setUp(self):
        logging.disable(logging.CRITICAL)

    def tearDown(self):
        logging.disable(logging.NOTSET)

    def fake_request(url, timeout=None):
        class FakeRequest(object):
            status_code = 200
            text = '<blockquote><p>test quote123</p></blockquote>'

            def close(self):
                pass

            def raise_for_status(self):
                pass
        return FakeRequest()

    @mock.patch('requests.get', fake_request)
    def test_getquote_new_quote(self):
        call_command('getquote')

        quote = Quote.objects.all().order_by('-pk')[0]
        self.assertEqual(quote.quote, 'test quote123')

    @mock.patch('requests.get', fake_request)
    def test_getquote_already_exists(self):
        call_command('getquote')
