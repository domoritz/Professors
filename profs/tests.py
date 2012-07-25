import unittest

from pyramid import testing
from pyramid.testing import DummyRequest
from pyramid.testing import DummyResource
from pyramid.compat import url_quote, url_unquote

class ViewTests(unittest.TestCase):
	def setUp(self):
		self.config = testing.setUp()

	def tearDown(self):
		testing.tearDown()

	def test_home_view(self):
		from .views import home_view
		request = DummyRequest()
		response = home_view(request)
		self.assertEqual(response['project'], 'Professors')

	def test_results_view(self):
		from .views import results_view
		request = DummyRequest()
		q = 'foo bar'
		request.matchdict = {'query': q}
		response = results_view(request)

		self.assertEqual(response['query'], q)


class FunctionalTests(unittest.TestCase):
    def setUp(self):
        from . import main

        app = main(None, static_assets = "static")
        from webtest import TestApp

        self.testapp = TestApp(app)

    def test_unexisting_page(self):
        res = self.testapp.get('/SomePage', status=404)
        self.assertTrue('Not Found' in res.body)

    def test_home_page(self):
        res = self.testapp.get('/', status=200)
        self.failUnless('id="home"' in res.body)

    def test_redirection_search(self):
    	q = 'foo bar'
        res = self.testapp.post('/search?query=foo bar', status=302)
        self.assertEqual(res.location, 'http://localhost/find/'+url_quote(q))

    def test_results_page(self):
        res = self.testapp.get('/find/abc', status=200)
        self.failUnless('id="results"' in res.body)




